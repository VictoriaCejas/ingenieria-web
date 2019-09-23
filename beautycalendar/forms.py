from django import forms
from .models import Users, ContentUsers, Empleoyees, WorkItems, BeautySalons
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Nombre')
    last_name = forms.CharField(max_length=30, label='Apellido')
    Choices = [('bussines', 'Bussines')]
    bussines = forms.BooleanField(required=False, initial=False, label='Bussines', help_text='Cuenta para emprendedor',)

    #class Meta:
     #   model=User
      #  fields=['bussines']

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class ContentForm(forms.ModelForm):
    paused= forms.BooleanField(required=False)
    class Meta:
        model = ContentUsers
        fields = ['user','category','title','imageProduct','price','state']
        widgets = {'user':forms.HiddenInput(),'category':forms.HiddenInput(), 'state':forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['user'].required= False
        self.fields['category'].required= False
 

class EmpleoyeesForm(forms.ModelForm):
    paused= forms.BooleanField(required=False)
    class Meta:
        model= Empleoyees
        fields= ['boss','first_name','last_name','imageEmpleoyee','state']
        widgets= {'boss':forms.HiddenInput(),'state':forms.HiddenInput()}
   
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['boss'].required= False
    
class AvatarForm(forms.ModelForm):
    
    class Meta:
        model=Users
        fields=['imageAvatar']

class FrontForm(forms.ModelForm):
    class Meta:
        model= Users
        fields=['imageFront']


class BeautySalonsForm(forms.ModelForm):
    class Meta:
        model= BeautySalons
        fields=['owner','items']
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['owner'].required= False

class BioForm(forms.ModelForm):
    items= forms.ModelMultipleChoiceField(queryset=WorkItems.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model= Users
        fields=['first_name','description']

