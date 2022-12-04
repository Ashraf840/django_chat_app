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
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            # Raise auth-error where this form gets rendered
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Credentials! Please insert correct email & password.")

    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs['class'] = 'form-control'
    #     self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
    #     self.fields['password'].widget.attrs['class'] = 'form-control'
    #     self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
