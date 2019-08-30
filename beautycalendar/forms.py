from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, UserForm
from allauth.account.signals import email_confirmed, user_signed_up
from django.dispatch import receiver
from allauth.account.adapter import DefaultAccountAdapter


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    Choices = [('bussines', 'Bussines')]
    bussines = forms.BooleanField(required=False, initial=False, label='Bussines', help_text='Cuenta para emprendedor',)

    class Meta:
        model=Usuario
        fields=['bussines']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user

    
'''
class EmailValidationOnForgotPassword(ResetPasswordForm):
    username = forms.CharField(max_length=255, required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        usernamef = self.cleaned_data.get('username')
      #  if not User.objects.filter(email__iexact=email,username=usernamef, is_active=True).exists():
      #      raise forms.ValidationError("Esta direccion no esta registrada!")
      #  return email
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:   
            raise forms.ValidationError("Datos mal ingresados!")
        except MultipleObjectsReturned:
            raise forms.ValidationError("Logueate con tu red social!")
       
        return email

'''