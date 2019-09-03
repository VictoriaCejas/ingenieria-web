from django.db import models
from django.contrib.auth.models import User
from allauth.account.signals import email_confirmed, user_signed_up
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from django.dispatch import Signal
# Create your models here.
'''
class TiposUsuario(models.Model):
    #Tipo de usuario: Admin, Bussines, Client
    idTipoUsuario= models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length=50, null=False, blank=False)
    
    def __str__(self):
        return self.descripcion
    
class EstadosUsuario(models.Model):
    #Estados de usuario, pueden ser: Activo, bloqueado,..
    idEstadoUsuario= models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length= 50, null=False, blank=False)
    def __str__(self):
        return self.descripcion
'''

class Usuario(models.Model):
    bussines=1
    cliente= 2
    administrador= 3
    tipoChoices= (
        (bussines,'bussines'),
        (cliente,'cliente'),
        (administrador,'administrador'),
    )
    activo= 1
    pendienteactivacion=2
    bloqueado= 3
    eliminado=4
    estadosChoices= (
        (activo,'activo'),
        (pendienteactivacion,'pendiente de activacion'),
        (bloqueado,'bloqueado'),
        (eliminado, 'eliminado'),
    )
    #usuario modificado
    #crea un nuevo modelo que se enlaza con el USER
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    correo = models.EmailField()
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False,null=False)
    #estado = models.ForeignKey(EstadosUsuario, on_delete=models.CASCADE)
    estado= models.PositiveSmallIntegerField(choices=estadosChoices)
    #tipo = models.ForeignKey(TiposUsuario, on_delete=models.CASCADE)
    tipo= models.PositiveSmallIntegerField(choices=tipoChoices)
    reputacion= models.PositiveSmallIntegerField(null=True)
    imagenAvatar= models.ImageField(null=True,blank=True,upload_to='avatar_image')
    imagenPortada= models.ImageField(null=True,blank=True,upload_to='front_image')

    def __str__(self):
        return self.nombre 
    

@receiver(user_signed_up)
def sing_up(request,user,**kwargs):
    #Cuando se recibe señal de registro exitoso, se guarda en usuario en el modelo Usuario.
    #import web_pdb; web_pdb.set_trace()
    activo= 1
    pendienteactivacion=2
    bussines= 1
    cliente= 2
    nombre = user.first_name
    apellido=user.last_name
    estadoUsuario=0
    tipoUsuario=0
   # import web_pdb; web_pdb.set_trace()
    if request.method=="POST":
        form= request.POST
        #estado = EstadosUsuario.objects.get(descripcion='pendiente activacion') 
        try:
            form['bussines']
            tipoUsuario= bussines
            #tipo = TiposUsuario.objects.get(descripcion='bussines')
        except:
            tipoUsuario=cliente
            #tipo = TiposUsuario.objects.get(descripcion='cliente')
        estadoUsuario = pendienteactivacion
    else:
        estadoUsuario= activo
        tipoUsuario= cliente
        #estado = EstadosUsuario.objects.get(descripcion='activo') 
        #tipo = TiposUsuario.objects.get(descripcion='cliente')

    # import web_pdb; web_pdb.set_trace()
    us = Usuario(usuario=user, correo=user.email, nombre=nombre, apellido=apellido, estado=estadoUsuario, tipo=tipoUsuario, reputacion=0)
    us.save()


@receiver(email_confirmed)
def confirm_user(request,email_address,**kwargs):
#Cuando se recibe la señal de confirmacion de mail, cambia el estado del usuario
    try:
        user = User.objects.get(email=email_address.email)
    except(TypeError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None:
        activo= 1
        user.is_active = True
        user.save()
        #estadoActivado = EstadosUsuario.objects.get(descripcion='activo')
        usuario = Usuario.objects.get(usuario=user)
        #usuario.estado = estadoActivado
        usuario.estado= activo
        # Guarda usuario como activo
        usuario.save()
       

