from django.urls import path

from users.views import register, ProfileDetailView, ProfileFollowView
from django.contrib.auth import views as auth_views

urlpatterns = [
       path('register', register, name="user-register"),
       path("login", auth_views.LoginView.as_view(template_name='users/login.html'), name="user-login" ),
       path("logout", auth_views.LogoutView.as_view(template_name='users/logout.html'), name="user-logout"),
       path("password-reset",
            auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
            name="password_reset"),

       path("password-reset-confirm/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
            name="password_reset_confirm"),

       path("password-reset-done",
            auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
            name="password_reset_done"),

       path("password-reset-complete",
            auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
            name="password_reset_complete"),

       path("password-change",
            auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'),
            name="password_change"),

       path("password-change-done",
            auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
            name="password_change_done"),

       path("profile", ProfileDetailView.as_view(), name="user-profile"),
       path("follow", ProfileFollowView.as_view(), name="user-follow"),
]
