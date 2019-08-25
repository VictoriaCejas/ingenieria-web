from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario
    

class SignupForm(UserCreationForm):
   
    email = forms.EmailField(max_length=200, help_text='Required')
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'nombre','apellido','password1', 'password2')

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