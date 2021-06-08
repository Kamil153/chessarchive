from django.urls import path
from django.views.generic import TemplateView
from .views import EditProfileView, GameList, GameDetailView, FriendList
from . import views

urlpatterns = [
    path('', FriendList.as_view(template_name='home.html'), name='home'),
    path('profile/', EditProfileView.as_view(), name='profile'),
    path('game/', GameList.as_view(template_name='list.html'), name='game-list'),
    path('game/add', views.AddGameView.as_view(), name='game-add'),
    path('game/<int:pk>/', GameDetailView.as_view(template_name='details.html'), name='details'),
    path('game/<int:pk>/delete', views.GameDeleteView.as_view(), name='game-delete'),
    path('invite/<username>/', views.send_invitation, name='send-invitation'),
    path('accept/<username>', views.accept_invitation, name='accept'),
    path('reject/<username>', views.reject_invitation, name='reject')
]
