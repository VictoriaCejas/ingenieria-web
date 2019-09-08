from django.db import models
from allauth.account.signals import email_confirmed, user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.dispatch import Signal
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)
from allauth.socialaccount.signals import pre_social_login
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
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


class User(AbstractBaseUser):
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
    imageAvatar= models.ImageField(null=True,blank=True,upload_to='avatar_image')
    imageFront= models.ImageField(null=True,blank=True,upload_to='front_image')
    description= models.CharField(max_length=250,blank=True, null=True)

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

class ContentUser(models.Model):
    """
    Products&Services 
    """
    product= 1
    service= 2
    categoryChoices= (
        (product,'producto'),
        (service,'servicio'),
    )
    user= models.ForeignKey('User',on_delete=models.CASCADE)
    category= models.PositiveSmallIntegerField(choices=categoryChoices, blank=False, null=False)
    title= models.CharField(max_length=50, blank=False, null=False)
    imageProduct= models.ImageField(blank=True, null=True, upload_to='Products')
    description= models.CharField(blank=True, null=True,max_length=100) #cambiar por precio
       
    def __str__(self):
        return self.title 
        
#SEÑALES ALLAUTH
@receiver(user_signed_up)
def sing_up(request,user,**kwargs):
    #Cuando se recibe señal de registro exitoso, se guarda en usuario en el modelo Usuario.
    #import web_pdb; web_pdb.set_trace()
    active= 1
    pendingactivation=2
    bussines= 1
    client= 2
    stateUser=0
    kindUser=0
   # import web_pdb; web_pdb.set_trace()
    if request.method=="POST":
        form= request.POST
        #estado = EstadosUsuario.objects.get(descripcion='pendiente activacion') 
        try:
            form['bussines']
            kindUser= bussines
            #tipo = TiposUsuario.objects.get(descripcion='bussines')
        except:
            kindUser=client
            #tipo = TiposUsuario.objects.get(descripcion='cliente')
        stateUser = pendingactivation
        email=request.POST['email']
    else:
        stateUser= active
        kindUser= client
        #import web_pdb; web_pdb.set_trace()
        email=user

        #estado = EstadosUsuario.objects.get(descripcion='activo') 
        #tipo = TiposUsuario.objects.get(descripcion='cliente')

    # import web_pdb; web_pdb.set_trace()
    us=User.objects.get(email=email)
    us.state= stateUser
    us.kind= kindUser
    us.save()

@receiver(email_confirmed)
def confirm_user(request,email_address,**kwargs):
#Cuando se recibe la señal de confirmacion de mail, cambia el estado del usuario
    try:
        user = User.objects.get(email=email_address.email)
    except(TypeError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        active= 1
        user.state=active    
        user.save()

