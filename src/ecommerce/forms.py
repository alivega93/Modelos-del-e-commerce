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

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Nombre del producto"
                }
            ),

            "price": forms.NumberInput(
                attrs={
                    "placeholder": "Precio"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe tu producto",
                    "rows": 4
                }
            ),
        }


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