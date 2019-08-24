from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('register', views.register, name='register'),
    path('login',views.IniciarSesion, name='login'),
    path('logout', views.CerrarSesion,name='logout'),
    path('private',views.Private, name='private'),
    path('public', views.Public, name='public'),
  #  path('bussines_profile', views.bussines_profile,name='bussines_profile'),

]
