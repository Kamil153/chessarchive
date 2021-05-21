from django.urls import path
from django.views.generic import TemplateView
from .views import EditProfileView, GameList
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile/', EditProfileView.as_view(), name='profile'),
    path('game/', GameList.as_view(template_name='list.html'), name='list'),
    path('add_game_form_submission/', views.add_game_form_submission, name='add_game_form_submission'),
    path('add_game/', views.add_game, name='add_game')
]
