from user_service.email import confirm_email_view, email_confirmation
from .views import (
    register,
    user_login,
    user_logout,
    subscription_view,
)
from django.urls import path

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("subscriptions/", subscription_view, name="subscriptions"),
    path("confirm_email/<str:token>/", confirm_email_view, name="confirm_email"),
    path("success_signup/", email_confirmation, name="success_signup"),
]
