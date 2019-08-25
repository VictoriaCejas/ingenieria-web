from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('register', views.register, name='register'),
    path('login',views.IniciarSesion, name='login'),
    path('logout', views.CerrarSesion,name='logout'),
    path('private',views.Private, name='private'),
    path('public', views.Public, name='public'),
    path('singup',views.signup,name='singup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
  #  path('bussines_profile', views.bussines_profile,name='bussines_profile'),

]