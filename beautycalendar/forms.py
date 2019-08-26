from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.core.exceptions import MultipleObjectsReturned



class SignupForm(UserCreationForm):

    email = forms.EmailField(max_length=200, help_text='Required')
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    Choices = [('bussines', 'Bussines')]
    bussines = forms.BooleanField(
        required=False, initial=False, label='Bussines', help_text='Cuenta para emprendedor',)

    class Meta:
        model = User
        fields = ('username', 'email', 'nombre', 'apellido',
                  'password1', 'password2', 'bussines')

    def clean_email(self):
        # Get the email
        mail = self.cleaned_data.get('email')
        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=mail)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return mail
        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('Este mail ya esta en uso')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(
                "Los datos ingresados son incorrectos, prueba de nuevo")
        elif not user.is_active:
            raise forms.ValidationError('Tu cuenta aun no esta activada')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class EmailValidationOnForgotPassword(PasswordResetForm):
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

