from django.urls import path, include
from .api import RegisterAPI, LoginAPI
from knox import views as knox_views

urlpatterns = [
    path(r'api/auth/register', RegisterAPI.as_view()),
    path(r'api/auth/login', LoginAPI.as_view()),
    path(r'api/auth/logout', knox_views.LogoutView.as_view(), name='knox_logout')
]