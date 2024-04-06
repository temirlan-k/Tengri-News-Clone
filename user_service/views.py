from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from tengrinews.settings import EMAIL_HOST_USER
from .models import *
from user_service.forms import UserRegistrationForm, UserLoginForm, SubscriptionForm
from django.contrib.auth import get_user_model

User = get_user_model()


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .forms import UserRegistrationForm

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")

            user_created = User.objects.create_user(username=username, email=email, password=password)
            user_created.save()

            email_conf = EmailConfirmation.create(user_created)

            subject = 'Confirm email'
            token = email_conf.token
            message = render_to_string('html/email/confirmation_email.html', {'user': user_created, 'token': token})  
            recipient_list = [user_created.email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, html_message=message)
            messages.success(request, "Your account has been registered successfully. Please check your email for confirmation.")
            return redirect("success_signup")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = UserRegistrationForm()
    return render(request, "html/users/register.html", {"form": form})


def email_confirmation(request):
    return render(request, "html/email/success_sign_up.html")



# def register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password1")
#             email = form.cleaned_data.get("email")

#             EmailToken=EmailConfirmation.create()
#             token = profile.

#             user = authenticate(username=username, password=password)
#             messages.success(request, "Success!Please Check email to confirm account")

#             login(request, user)
#             return redirect("news_list")
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{error}")
#     else:
#         form = UserRegistrationForm()
#     return render(request, "html/users/register.html", {"form": form})


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


@login_required
def subscription_view(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            form.save_m2m()  
            return redirect('news_list')  
    else:
        form = SubscriptionForm(user=request.user)
    return render(request, 'html/users/subscriptions.html', {'form': form})


def confirm_email_view(request, token):
    try:
        user_email_token = EmailConfirmation.objects.get(token=token)
        user = user_email_token.user
        user.is_active = True
        user.save()
        messages.success(request, 'Your e-mail address has been successfully verified. You can now log in to your account.')
    except EmailConfirmation.DoesNotExist:
        messages.error(request, 'Invalid Token')
    return redirect('login')  
