from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name='home'),
    path('perfil', views.Perfil, name='perfil'),
    path('login',views.IniciarSesion, name='login'),
    path('logout', views.CerrarSesion,name='logout'),
    path('private',views.Private, name='private'),
    path('public', views.Public, name='public'),
    path('singup',views.Signup,name='singup'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.Activate, name='activate'),
   # path('accounts/password_reset/',views.ResetPassword,name='reset_password')
   # path('accounts/', include('django.contrib.auth.urls')),
]