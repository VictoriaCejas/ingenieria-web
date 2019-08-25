from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TiposUsuario(models.Model):
    '''Tipo de usuario: Admin, Bussines, Client'''
    idTipoUsuario= models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length=50, null=False, blank=False)
    
class EstadosUsuario(models.Model):
    '''Estados de usuario, pueden ser: Activo, bloqueado,..'''
    idEstadoUsuario= models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length= 50, null=False, blank=False)


class Usuario(models.Model):
    #usuario modificado
    #crea un nuevo modelo que se enlaza con el USER
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    correo = models.EmailField()
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False,null=False)
    estado = models.ForeignKey(EstadosUsuario, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TiposUsuario, on_delete=models.CASCADE)
    token = models.CharField(max_length = 40, blank = True, null = True)
    reputacion= models.PositiveSmallIntegerField()

    