from django import forms
from .models import Users, ContentUsers, Empleoyees, WorkItems, BeautySalons, Publications,Reports, Draws
from allauth.account.forms import SignupForm
from django_resized import ResizedImageField
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


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
    sunday=1
    monday=2
    tuesday=3
    wednesday=4
    thursday=5
    friday=6
    saturday=7
    daysChoices= (
        (sunday,'domingo'),
        (monday,'lunes'),
        (tuesday,'martes'),
        (wednesday,'miercoles'),
        (thursday,'jueves'),
        (friday,'viernes'),
        (saturday,'sabado'),
    )
    items= forms.ModelMultipleChoiceField(queryset=WorkItems.objects.all(),required=False,widget=forms.CheckboxSelectMultiple)
    initDay= forms.ChoiceField(choices=daysChoices)
    endDay= forms.ChoiceField(choices=daysChoices)
    class Meta:
        model= Users
        fields=['first_name','last_name','name_salon','description',"items","initDay","endDay",]
   
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['first_name'].required= False
        self.fields['name_salon'].required= False
        self.fields['last_name'].required=False
        self.fields['description'].required=False
        self.fields['items'].required=False
        self.fields['initDay'].required=False
        self.fields['endDay'].required=False
        

class DatesUserForm(forms.Form):
    #service= forms.CharField(max_length=50)
   
    services= forms.ChoiceField(choices=(),required=True, initial="Seleccione")
    date= forms.DateTimeField(input_formats=['%d/%m/%Y'])

    def __init__(self, empleoyees_choices,services_choices, *args, **kwargs):
        super(DatesUserForm, self).__init__(*args, **kwargs)
        self.fields['empleoyees'].choices = empleoyees_choices
        self.fields['services'].choices= services_choices
    empleoyees = forms.ChoiceField(choices=(), required=True,initial="Seleccione")

class PublicationForm(forms.ModelForm):
    class Meta:
        model=Publications
        fields=['owner','publish_date','imagePublication','description','score','state']
        widgets={'owner':forms.HiddenInput(),'publish_date':forms.HiddenInput(),'score':forms.HiddenInput(),'state':forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['owner'].required= False
        self.fields['publish_date'].required= False

class PublForm(forms.Form):
    description= forms.CharField(max_length=250)
    imgPublication= forms.FileField()
    

class ReportsForm(forms.ModelForm):
    
    choices_report=(
        (1,'Mal servicio'),
        (2,'Precios desactualizados'),
        (3,'No cumple con los turnos'),
        (4,'Otro'),
    )
    
    options= forms.ChoiceField(choices=choices_report,required=True, initial="Seleccione")
    
    class Meta:
        model= Reports
        fields=['options','other']
        # widgets={'other':forms.HiddenInput()}

class DrawsForm(forms.ModelForm):
    class  Meta:
      model=Draws   
      fields=['name','description']
      widgets={
          'description': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '250px'}}),
      }
      def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['owner'].required= False
