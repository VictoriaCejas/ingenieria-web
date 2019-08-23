from django.contrib import admin
from .models import Usuario, Tipo_Usuario, Estado_Usuario
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Tipo_Usuario)
admin.site.register(Estado_Usuario)