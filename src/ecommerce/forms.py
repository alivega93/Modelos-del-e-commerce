from django import forms
from django.contrib.auth.models import User

from .models import ProductModel


class ProductModelForm(forms.ModelForm):

    class Meta:
        model = ProductModel
        fields = [
            "title",
            "price",
            "description",
        ]


class UserRegistrationForm(forms.ModelForm):

    username = forms.CharField(
        label="Username",
        max_length=150,
        help_text=""
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text=""
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
        ]