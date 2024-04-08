from user_service.email import confirm_email_view, email_confirmation
from .views import (
    register,
    user_login,
    user_logout,
    subscription_view,
)
from django.urls import path

urlpatterns = [
    path("user/register/", register, name="register"),
    path("user/login/", user_login, name="login"),
    path("user/logout/", user_logout, name="logout"),
    path("user/subscriptions/", subscription_view, name="subscriptions"),
    path("user/confirm_email/<str:token>/", confirm_email_view, name="confirm_email"),
    path("user/success_signup/", email_confirmation, name="success_signup"),
]
