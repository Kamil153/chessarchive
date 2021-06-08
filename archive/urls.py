from django.urls import path
from django.views.generic import TemplateView
from .views import EditProfileView, GameList, GameDetailView, FriendList
from . import views

urlpatterns = [
    path('', FriendList.as_view(template_name='home.html'), name='home'),
    path('profile/', EditProfileView.as_view(), name='profile'),
    path('game/', GameList.as_view(template_name='list.html'), name='list'),
    path('add_game_form_submission/', views.add_game_form_submission, name='add_game_form_submission'),
    path('add_game/', views.add_game, name='add_game'),
    path('game/<int:pk>/', GameDetailView.as_view(template_name='details.html'), name='details'),
    path('delete_game/<game_id>/', views.delete_game, name='delete-game'),
    path('send_invitation/<username>/', views.send_invitation, name='send-invitation'),
    path('accept/<username>', views.accept_invitation, name='accept'),
    path('reject/<username>', views.reject_invitation, name='reject')
]
