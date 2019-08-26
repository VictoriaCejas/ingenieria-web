from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario
from django.contrib.auth import authenticate, login

class SignupForm(UserCreationForm):
   
    email = forms.EmailField(max_length=200, help_text='Required')
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    Choices =[('bussines', 'Bussines')]
    bussines= forms.BooleanField(required=False,initial=False,label='Bussines',help_text='Cuenta para emprendedor',)
    class Meta:
        model = User
        fields = ('username', 'email', 'nombre','apellido','password1', 'password2','bussines')

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
            raise forms.ValidationError("Los datos ingresados son incorrectos, prueba de nuevo")
        elif not user.is_active:
            raise forms.ValidationError('Tu cuenta aun no esta activada')
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user