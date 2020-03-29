from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI
from knox import views as knox_views

urlpatterns = [
    path(r'api/auth', include('knox.urls')),
    path(r'api/auth/register', RegisterAPI.as_view()),
    path(r'api/auth/login', LoginAPI.as_view()),
    path(r'api/auth/user', UserAPI.as_view()),
    path(r'api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]