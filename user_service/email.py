from django.shortcuts import redirect, render
from user_service.models import EmailConfirmation
from django.contrib import messages


def confirm_email_view(request, token):
    try:
        user_email_token = EmailConfirmation.objects.get(token=token)
        user = user_email_token.user
        user.is_active = True
        user.save()
        messages.success(
            request,
            "Your e-mail address has been successfully verified. You can now log in to your account.",
        )
    except EmailConfirmation.DoesNotExist:
        messages.error(request, "Invalid Token")
    return redirect("login")


def email_confirmation(request):
    return render(request, "html/email/success_sign_up.html")
