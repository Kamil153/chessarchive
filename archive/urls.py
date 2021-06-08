from django.urls import path
from . import views

urlpatterns = [
    path('', views.FriendList.as_view(template_name='home.html'), name='home'),
    path('profile/', views.EditProfileView.as_view(), name='profile'),
    path('game/', views.GameList.as_view(template_name='list.html'), name='game-list'),
    path('game/add', views.AddGameView.as_view(), name='game-add'),
    path('game/<int:pk>/', views.GameDetailView.as_view(template_name='details.html'), name='details'),
    path('game/<int:pk>/delete', views.GameDeleteView.as_view(), name='game-delete'),
    path('game/<int:pk>/share', views.share, name='game-share'),
    path('game/<int:pk>/unshare', views.unshare, name='game-unshare'),
    path('user/<username>/game/', views.GameList.as_view(template_name='list.html'), name='user-game-list'),
    path('invite/<username>/', views.send_invitation, name='send-invitation'),
    path('accept/<username>', views.accept_invitation, name='accept'),
    path('reject/<username>', views.reject_invitation, name='reject')
]
