from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views import generic
from archive.models import ChessGame, ChessPlayer, PlayerDetail, GameTime, Movement

from django.shortcuts import render, redirect
import chess.pgn
import chess
import chess.svg
import io


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class EditProfileView(generic.UpdateView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'profile.html'
    fields = ['email', 'username']

    def get_object(self, queryset=None):
        return self.request.user


class GameList(generic.ListView, LoginRequiredMixin):
    model = ChessGame

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


def add_game(request):
    return render(request, "add_game.html")


def add_game_form_submission(request):
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

    if len(moves_list) % 2 != 0:
        moves_list.append("end_game")

    i, j = 1, 0
    while j < len(moves_list):
        move_to_insert = Movement(game=game, move_nr=i, white_move=moves_list[j], black_move=moves_list[j + 1])
        move_to_insert.save()
        i += 1
        j += 2

    return render(request, "add_game.html")


class GameDetailView(generic.DetailView):
    model = ChessGame

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game: ChessGame = context['object']
        context['sorted_moves'] = game.movement_set.order_by('move_nr')
        context['svg_list'] = self.svg_list(context)
        context['svg'] = chess.svg.board(chess.Board(), size=400)
        return context

    def svg_list(self, context):
        moves_list = self.get_moves_list(context['sorted_moves'])
        board = chess.Board()
        svg_list = [chess.svg.board(chess.Board(), size=400)]
        for move in moves_list:
            if move != 'end_game':
                board.push_san(move)
                svg_list.append(chess.svg.board(board, size=400))

        return svg_list

    def get_moves_list(self, context):
        moves_list = []
        for move in context:
            moves_list.append(move.white_move)
            moves_list.append(move.black_move)
        return moves_list


def delete_event(request, game_id):
    game = ChessGame.objects.get(id=game_id)
    game.delete()

    movement = Movement.objects.filter(game=game_id)
    for move in movement:
        move.delete()

    player_details = PlayerDetail.objects.filter(game=game_id)
    for detail in player_details:
        detail.delete()

    return redirect('list')  # list-events


def sort_by(request):
    selected_option = request.POST.get('sorting_options', False)
    games = ChessGame.objects.all()
    if selected_option is not False:
        if selected_option == 'note - asc':
            games = ChessGame.objects.order_by('note')
        elif selected_option == 'note - desc':
            games = ChessGame.objects.order_by('-note')

        elif selected_option == 'date - asc':
            games = ChessGame.objects.order_by('game_date')
        elif selected_option == 'date - desc':
            games = ChessGame.objects.order_by('-game_date')

        elif selected_option == 'game time - asc':
            games = ChessGame.objects.order_by('game_time')
        elif selected_option == 'game time - desc':
            games = ChessGame.objects.order_by('-game_time')

        context = {
            'object_list': games
        }
        return render(request=request, template_name='list.html', context=context)
    return redirect('list')


def filter_by(request):
    player_name = request.POST.get('player_name', False)
    date_from = request.POST.get('date_from', False)
    date_to = request.POST.get('date_to', False)
    ranking_from = request.POST.get('ranking_from', False)
    ranking_to = request.POST.get('ranking_to', False)
    game_time = request.POST.get('game_time', False)
    first_move = request.POST.get('first_move', False)
    games = ChessGame.objects.all()

    if player_name != '':
        games = games.filter(playerdetail__player__name=player_name)
    if date_from != '':
        games = games.filter(game_date__gte=date_from)
    if date_to != '':
        games = games.filter(game_date__lte=date_to)
    if ranking_from != '':
        games = games.filter(playerdetail__rate__gte=ranking_from)
    if ranking_to != '':
        games = games.filter(playerdetail__rate__lte=ranking_to)
    if game_time != '':
        time = GameTime.objects.get(game_time=game_time)
        games = games.filter(game_time=time)
    if first_move != '':
        games = games.filter(movement__move_nr=1, movement__white_move=first_move)

    context = {
        'object_list': games
    }
    return render(request=request, template_name='list.html', context=context)
