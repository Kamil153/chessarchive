from django.contrib import admin
from django.urls import path, include

from archive.views import SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('archive.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
]
