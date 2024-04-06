from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.models import User

from news_service.models import Category
from user_service.models import Subscription


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["categories"]
        widgets = {"categories": forms.CheckboxSelectMultiple}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["categories"].queryset = Category.objects.all()
