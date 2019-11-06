from django.db import models
from allauth.account.signals import email_confirmed, user_signed_up, password_reset
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser
from django.core.validators import MaxValueValidator
from django_resized import ResizedImageField
from rest_framework.authtoken.models import Token

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, kind, state, password=None):
        """
        Creates and saves a User with the given email, kind,
        state and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            kind=kind,
            state=state,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        Set by default kind and state.

        """
        user = self.create_user(
            email,
            password=password,
            kind=3,
            state=1,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    """
    User created with abstractUser for replace the default.
    """
    bussines=1
    client= 2
    administrator= 3
    kindsChoices= (
        (bussines,'bussines'),
        (client,'client'),
        (administrator,'administrator'),
    )
    active= 1
    pendingactivation=2
    locked= 3
    removed=4
    statesChoices= (
        (active,'active'),
        (pendingactivation,'pending activation'),
        (locked,'locked'),
        (removed, 'removed'),
    )
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False,null=False)
    state= models.PositiveSmallIntegerField(choices=statesChoices, blank=True, null=True)
    kind= models.PositiveSmallIntegerField(choices=kindsChoices, blank=True, null=True)
    score= models.PositiveSmallIntegerField(null=True)
   # imageAvatar= models.ImageField(null=True,blank=True,upload_to='avatar_image')
    imageAvatar = ResizedImageField(size=[150, 150], quality=90, crop=['middle', 'center'], upload_to='avatar_image',blank=True, null=True)
   # imageFront= models.ImageField(null=True,blank=True,upload_to='front_image')
    imageFront = ResizedImageField(size=[1281, 236], quality=90, crop=['middle', 'center'], upload_to='front_image',blank=True, null=True)    
    description= models.CharField(max_length=250,blank=True, null=True)
    name_salon= models.CharField(max_length=50, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
   
    class Meta:
        verbose_name = 'Users'
        verbose_name_plural = 'Users'

class ContentUsers(models.Model):
    """
    Products&Services 
    """
    product= 1
    service= 2
    categoryChoices= (
        (product,'product'),
        (service,'service'),
    )
    active= 1
    paused=2
    removed=3
    statesChoices= (
        (active,'active'),
        (paused,'paused'),
        (removed,'removed'),
    )
    user= models.ForeignKey('Users',on_delete=models.CASCADE)
    category= models.PositiveSmallIntegerField(choices=categoryChoices, blank=False, null=False)
    title= models.CharField(max_length=50, blank=False, null=False)
    #imageProduct= models.ImageField(blank=True, null=True, upload_to='Products')
    imageProduct = ResizedImageField(size=[100, 100], quality=90, crop=['middle', 'center'], upload_to='Products',blank=True, null=True)
    
    price= models.FloatField(blank=True, null=True) #cambiar por precio
    state= models.PositiveSmallIntegerField(choices= statesChoices, blank=True, null=True)
    attention_time= models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title 

    class Meta:
        verbose_name = 'Content users'  
        verbose_name_plural = 'Content users'

class Empleoyees(models.Model):
    active= 1
    paused=2
    removed=3
    statesChoices= (
        (active,'active'),
        (paused,'paused'),
        (removed,'removed'),
    )
    boss= models.ForeignKey('Users', on_delete=models.CASCADE)
    first_name= models.CharField(max_length=50, blank=False, null=False)
    last_name= models.CharField(max_length=50, blank=False, null=False)
    imageEmpleoyee = ResizedImageField(size=[100, 100], quality=90, crop=['middle', 'center'], upload_to='Employees',blank=True, null=True)

    state= models.PositiveSmallIntegerField(choices= statesChoices, blank=True, null=True)

    def __str__(self):
        return self.first_name
    class Meta:
        verbose_name = 'Empleoyees'
        verbose_name_plural = 'Empleoyees'

class WorkItems (models.Model):
    item= models.CharField(max_length=50, blank=True,null=True)
    def __str__(self):
        return self.item
    class Meta:
        verbose_name = 'Work items'  
        verbose_name_plural = 'Work items'

class BeautySalons(models.Model):
    owner= models.ForeignKey('Users', on_delete=models.CASCADE)
    items= models.ForeignKey('WorkItems', on_delete= models.CASCADE)
    class Meta:
        verbose_name = 'Salons'  
        verbose_name_plural = 'Salons'

class Publications(models.Model):
    active= 1
    locked=2
    removed=3
    statesChoices= (
        (active,'active'),
        (locked,'locked'),
        (removed,'removed'),
    )
    owner= models.ForeignKey('Users', on_delete=models.CASCADE)
    publish_date= models.DateTimeField(blank=False, null=False) #Fecha y hora
  #  imagePublication= models.ImageField(blank=False, null=False, upload_to='Publications')
    imagePublication= ResizedImageField(size=[300, 300], quality=90, crop=['middle', 'center'], upload_to='Publications',blank=True, null=True)
    description= models.CharField(max_length=250, blank=True, null=True)
    score= models.PositiveIntegerField(blank=True, null=True)
    state= models.PositiveSmallIntegerField(choices= statesChoices, blank=True, null=True)

class LikesPublications(models.Model):
    #True is Like , False Dislike
    publication= models.ForeignKey('Publications', on_delete= models.CASCADE)
    user= models.ForeignKey('Users', on_delete=models.CASCADE)
    value=models.NullBooleanField(blank=True, null=True)
    class Meta:
        unique_together = (("publication", "user"),)

class CommentsPublications(models.Model):
    publication= models.ForeignKey('Publications',on_delete=models.CASCADE)
    user= models.ForeignKey('Users', on_delete=models.CASCADE)
    date= models.DateTimeField(blank=False, null=False)
    comment= models.CharField(max_length=250,blank=False,null=False)

class WorkingHoursSalons(models.Model):
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

    #empleoyee= models.ForeignKey('Empleoyees',on_delete=models.CASCADE)
    salon= models.ForeignKey('Users',on_delete=models.CASCADE)
    init_date= models.PositiveSmallIntegerField(choices=daysChoices, blank=False, null=False,validators=[MaxValueValidator(6)]) #0 domingo.. 6 sabado
    finish_date= models.PositiveSmallIntegerField(choices=daysChoices, blank=False, null=False, validators=[MaxValueValidator(6)]) #0 domingo.. 6 sabado
    init_time= models.DateTimeField(blank=True, null=True)
    finish_time= models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Working hours salons'
        verbose_name_plural = 'Workin hours salons'

class UserDates(models.Model):
    confirmed= 1
    cancelled=2
    finalized=3
    statesChoices= (
        (confirmed,'confirmed'),
        (cancelled,'cancel'),
        (finalized,'finalized'),
    )
    client= models.ForeignKey('Users', on_delete=models.CASCADE)
    date= models.DateField(blank=False, null=False)
    service= models.ForeignKey('ContentUsers', on_delete=models.CASCADE)
    empleoyee= models.ForeignKey('Empleoyees', on_delete= models.CASCADE)
    salon= models.CharField(max_length=50)
    state= models.PositiveSmallIntegerField(choices= statesChoices, blank=True, null=True)
    init_time= models.DateTimeField(blank=True, null=True)
    finish_time= models.DateTimeField(blank=True, null=True)
    class Meta:
        verbose_name = 'Dates'
        verbose_name_plural = 'Dates'

class Reports(models.Model):
    
    choices_report=(
        (1,'Mal servicio'),
        (2,'Precios desactualizados'),
        (3,'No cumple con los turnos'),
        (4,'Otro'),
    )
    informer = models.EmailField(blank=False, null=False)
    informed= models.EmailField(blank=False, null=False)
    options= models.PositiveSmallIntegerField(choices=choices_report,blank=False, null=False)
    other= models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        verbose_name = 'Reports'
        verbose_name_plural = 'Reports'
        
class Draws(models.Model):
    actived= 1
    finalized=2
    statesChoices= (
        (actived,'actived'),
        (finalized,'finalized'),
    )
    name= models.CharField(max_length=50, blank=False, null=False)
    owner= models.ForeignKey('Users',on_delete=models.CASCADE)
    finish_day= models.DateTimeField(blank=False, null=False)
    state= models.PositiveSmallIntegerField(choices= statesChoices, blank=True, null=True)
    description= models.TextField(max_length=250, blank=True, null=True)
    class Meta:
        verbose_name = 'Draws'
        verbose_name_plural = 'Draws'

    
class DrawsList(models.Model):
    draw= models.ForeignKey('Draws',on_delete=models.CASCADE)
    client= models.ForeignKey('Users',on_delete=models.CASCADE)
    class Meta:
        unique_together = (("draw", "client"),)
        verbose_name = 'Lists draws'
        verbose_name_plural = 'Lists draws'

    
    
#SEÑALES ALLAUTH
@receiver(user_signed_up)
def sing_up(request,user,**kwargs):
    #Cuando se recibe señal de registro exitoso, se guarda en usuario en el modelo Usuario.
    """Cuando se recive la señal de registro exitoso, se guarda en usuarios el modelo
    de usuario, ademas, si el usuario es bussines, crea el salon correspondiente a este"""
    active= 1
    pendingactivation=2
    bussines= 1
    client= 2
    stateUser=0
    kindUser=0
    if request.method=="POST":
        form= request.POST
        try:
            form['bussines']
            kindUser= bussines
        except:
            kindUser=client
            #tipo = TiposUsuario.objects.get(descripcion='cliente')
        stateUser = pendingactivation
        email=request.POST['email']
    else:
        stateUser= active
        kindUser= client
        email=user
    us=Users.objects.get(email=email)
    us.state= stateUser
    us.kind= kindUser
    us.save()
    """Crear token para api"""
    Token.objects.create(user=us)
    
@receiver(email_confirmed)
def confirm_user(request,email_address,**kwargs):
    #Cuando se recibe la señal de confirmacion de mail, cambia el estado del usuario
    try:
        user = Users.objects.get(email=email_address.email)
    except(TypeError, OverflowError, Users.DoesNotExist):
        user = None
    if user is not None:
        active= 1
        user.state=active    
        user.save()


