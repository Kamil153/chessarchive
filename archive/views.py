from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from archive.models import ChessGame


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


class GameDetailView(generic.DetailView):
    model = ChessGame

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game: ChessGame = context['object']
        context['sorted_moves'] = game.movement_set.order_by('move_nr')
        return context

