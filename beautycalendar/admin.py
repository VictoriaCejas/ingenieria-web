from django.contrib import admin
from .models import Usuario, TiposUsuario, EstadosUsuario
# Register your models here.
admin.site.register(Usuario)
admin.site.register(TiposUsuario)
admin.site.register(EstadosUsuario)
