from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import get_user_model

from tengrinews.settings import EMAIL_HOST_USER
from user_service.forms import UserRegistrationForm, UserLoginForm, SubscriptionForm
from user_service.models import EmailConfirmation

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")

            user_created = User.objects.create_user(
                username=username, email=email, password=password
            )
            user_created.save()

            email_conf = EmailConfirmation.create(user_created)
            subject = "Confirm email"
            token = email_conf.token
            message = render_to_string(
                "html/email/confirmation_email.html",
                {"user": user_created, "token": token},
            )
            recipient_list = [user_created.email]
            send_mail(
                subject, message, EMAIL_HOST_USER, recipient_list, html_message=message
            )

            messages.success(
                request,
                "Your account has been registered successfully. Please check your email for confirmation.",
            )
            return redirect("success_signup")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegistrationForm()
    return render(request, "html/users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            print(user)

            login(request, user)
            return redirect("search_news")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserLoginForm()
    return render(request, "html/users/login.html", {"form": form})


def user_logout(request):
    print(request)
    logout(request)
    return redirect("login")


@login_required(login_url="/user/login/")
def subscription_view(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            form.save_m2m()
            return redirect("news_list")
    else:
        form = SubscriptionForm(user=request.user)
    return render(request, "html/users/subscriptions.html", {"form": form})
