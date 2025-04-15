from django.urls import path

from users.views import register, profile
from django.contrib.auth import views as auth_views

urlpatterns = [
       path('register', register, name="user-register"),
       path("login", auth_views.LoginView.as_view(template_name='users/login.html'), name="user-login" ),
       path("logout", auth_views.LogoutView.as_view(template_name='users/logout.html'), name="user-logout"),
       path("profile", profile, name="user-profile")
]
