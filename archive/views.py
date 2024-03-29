from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse_lazy
from django.views import generic, View
from archive.models import ChessGame, ChessPlayer, PlayerDetail, GameTime, Movement, Profile

from django.shortcuts import render, redirect
import chess.pgn
import chess
import chess.svg
import io


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'profile.html'
    fields = ['email', 'username']

    def get_object(self, queryset=None):
        return self.request.user


class GameList(LoginRequiredMixin, generic.ListView):
    model = ChessGame

    def get_queryset(self):
        player_name = self.request.GET.get('player_name', None)
        date_from = self.request.GET.get('date_from', None)
        date_to = self.request.GET.get('date_to', None)
        ranking_from = self.request.GET.get('ranking_from', None)
        ranking_to = self.request.GET.get('ranking_to', None)
        game_time = self.request.GET.get('game_time', None)
        first_move = self.request.GET.get('first_move', None)
        selected_option = self.request.GET.get('sort_by', None)
        order = self.request.GET.get('order', None)
        username = self.kwargs.get('username', None)
        games = super().get_queryset()
        if username is not None:
            owner = User.objects.get(username=username)
            if owner is None:
                raise Http404()
            games = games.filter(user=owner, share=True)
        else:
            games = games.filter(user=self.request.user)

        if player_name:
            games = games.filter(playerdetail__player__name=player_name)
        if date_from:
            games = games.filter(game_date__gte=date_from)
        if date_to:
            games = games.filter(game_date__lte=date_to)
        if ranking_from:
            games = games.filter(playerdetail__rate__gte=ranking_from)
        if ranking_to:
            games = games.filter(playerdetail__rate__lte=ranking_to)
        if game_time:
            games = games.filter(game_time__game_time=game_time)
        if first_move:
            games = games.filter(movement__move_nr=1, movement__white_move=first_move)

        if selected_option and selected_option in ['note', 'game_date', 'game_time']:
            order_str = selected_option
            if selected_option == 'game_time':
                order_str += '__game_time'
            if order and order == 'desc':
                order_str = '-' + order_str
            games = games.order_by(order_str)

        return games

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_by'] = self.request.GET.get('sort_by', None)
        context['order'] = self.request.GET.get('order', None)
        context['private'] = False if 'username' in self.kwargs else True
        context['owner'] = self.kwargs.get('username', None)
        return context


class AddGameView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "add_game.html")

    def post(self, request):
        white_player = request.POST["whitePlayer"]
        black_player = request.POST["blackPlayer"]
        white_rank = request.POST["whiteRank"]
        black_rank = request.POST["blackRank"]
        time = request.POST["time"]
        increment = request.POST["increment"]
        date = request.POST["date"]
        moves = request.POST["moves"]
        note = request.POST["note"]
        user = request.user

        if not GameTime.objects.filter(game_time=time, time_increment=increment).exists():
            game_time = GameTime(game_time=time, time_increment=increment)
            game_time.save()
        else:
            game_time = GameTime.objects.get(game_time=time, time_increment=increment)

        game = ChessGame(user=user, game_time=game_time, note=note, game_date=date)
        game.save()

        if not ChessPlayer.objects.filter(name=white_player).exists():
            player1 = ChessPlayer(name=white_player)
            player1.save()
        else:
            player1 = ChessPlayer.objects.get(name=white_player)

        if not ChessPlayer.objects.filter(name=black_player).exists():
            player2 = ChessPlayer(name=black_player)
            player2.save()
        else:
            player2 = ChessPlayer.objects.get(name=black_player)

        detail1 = PlayerDetail(rate=white_rank, color="white", player=player1, game=game)
        detail1.save()
        detail2 = PlayerDetail(rate=black_rank, color="black", player=player2, game=game)
        detail2.save()

        # moves parsing
        pgn_file = io.StringIO(moves)
        game_moves = chess.pgn.read_game(pgn_file)
        node = game_moves
        moves_list = []
        while node.variations:
            next_node = node.variation(0)
            moves_list.append(str(node.board().san(next_node.move)))
            node = next_node

        result = game_moves.headers["Result"]
        moves_list.append(result)
        if len(moves_list) % 2 != 0:
            moves_list.append('')

        i, j = 1, 0
        while j < len(moves_list):
            move_to_insert = Movement(game=game, move_nr=i, white_move=moves_list[j], black_move=moves_list[j + 1])
            move_to_insert.save()
            i += 1
            j += 2

        return redirect('game-list')


class GameDetailView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = ChessGame

    def test_func(self):
        owner = self.get_object().user
        usr = self.request.user
        return owner == usr or (self.get_object().share and usr.profile in owner.profile.friends.all())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game: ChessGame = context['object']
        context['sorted_moves'] = game.movement_set.order_by('move_nr')
        context['svg_list'] = self.svg_list(context)
        context['svg'] = chess.svg.board(chess.Board(), size=400)
        context['result'] = self.get_result(context)
        context['allow_edit'] = True if game.user == self.request.user else False
        context['pk'] = self.kwargs['pk']
        return context

    def get_result(self, context):
        obj = context['sorted_moves'].last()
        if obj.white_move in ["1-0", "0-1", "1/2-1/2"]:
            return obj.white_move
        elif obj.black_move in ["1-0", "0-1", "1/2-1/2"]:
            return obj.black_move
        return '???'

    def svg_list(self, context):
        moves_list = self.get_moves_list(context['sorted_moves'])
        board = chess.Board()
        svg_list = [chess.svg.board(chess.Board(), size=400)]
        for move in moves_list:
            if move not in ["1-0", "0-1", "1/2-1/2", "*", ""]:  # '*' and '' when added string is not pgn
                board.push_san(move)
                svg_list.append(chess.svg.board(board, size=400))

        return svg_list

    def get_moves_list(self, context):
        moves_list = []
        for move in context:
            moves_list.append(move.white_move)
            moves_list.append(move.black_move)
        return moves_list


class GameDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = ChessGame
    success_url = reverse_lazy('game-list')


class FriendList(LoginRequiredMixin, generic.ListView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_users'] = User.objects.all()
        return context

    def get_object(self, queryset=None):
        return self.request.user

    def get_queryset(self):
        username = self.request.GET.get('username', None)
        users = super().get_queryset().exclude(user=self.request.user)

        if username:
            users = users.filter(user__username=username)

        return users


@login_required
def send_invitation(request, username):
    user_from = request.user.profile
    user_to = User.objects.get(username=username).profile

    if user_to is not None and user_from != user_to \
            and user_to not in user_from.friends.all() \
            and user_to not in user_from.invitations.all() \
            and user_from not in user_to.invitations.all():
        user_from.invitations.add(user_to)

    return redirect('home')


@login_required
def accept_invitation(request, username):
    user_from = request.user.profile
    user_to = User.objects.get(username=username).profile

    if user_to is not None and user_from != user_to and user_to in user_from.invitations_received.all():
        user_from.friends.add(user_to)
        user_to.invitations.remove(user_from)

    return redirect('home')


@login_required
def reject_invitation(request, username):
    user_from = request.user.profile
    user_to = User.objects.get(username=username).profile

    if user_to is not None and user_from != user_to and user_to in user_from.invitations_received.all():
        user_to.invitations.remove(user_from)

    return redirect('home')


@login_required
def share(request, pk):
    game = ChessGame.objects.get(pk=pk)
    if game.user != request.user:
        return redirect('home')
    game.share = True
    game.save()
    return redirect('details', pk)


@login_required
def unshare(request, pk):
    game = ChessGame.objects.get(pk=pk)
    if game.user != request.user:
        redirect('home')
    game.share = False
    game.save()
    return redirect('details', pk)
