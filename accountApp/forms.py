from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def save(self):
        user = super().save(commit=False)
        user.is_active = False
        user.save()
        return user


# Common User Login Form
class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # to hide the password-field-value while typing

    class Meta:
        model = User
        fields = ['email', 'password']

    def clean(self):
        # NB: use this func in order to make custom-validation of each/certain field(s)
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
        return self.cleaned_data
