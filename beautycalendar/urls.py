from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('perfil', views.Perfil, name='perfil'),
    path('private',views.Private, name='private'),
    path('public', views.Public, name='public'),

]