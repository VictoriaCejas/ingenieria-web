from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tipo_Usuario(models.Model):
    '''Tipo de usuario: Admin, Bussines, Client'''
    id_Tipo_Usuario= models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length=50, null=False, blank=False)
    
class Estado_Usuario(models.Model):
    '''Estados de usuario, pueden ser: Activo, bloqueado,..'''
    id_Estado_Usuario= models.AutoField(primary_key=True)
    descripcion= models.CharField(max_length= 50, null=False, blank=False)


class Usuario(models.Model):
    #usuario modificado
    #crea un nuevo modelo que se enlaza con el USER
    usuario= models.OneToOneField(User, on_delete=models.CASCADE)
    correo = models.EmailField()
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellido = models.CharField(max_length=50, blank=False,null=False)
    estado = models.ForeignKey(Estado_Usuario, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo_Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length = 40, blank = True, null = True)
    reputacion= models.PositiveSmallIntegerField()

    