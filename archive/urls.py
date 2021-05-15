from django.urls import path
from django.views.generic import TemplateView
from .views import EditProfileView


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('profile/', EditProfileView.as_view(), name='profile'),
]
