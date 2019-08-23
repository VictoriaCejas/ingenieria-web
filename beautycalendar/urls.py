from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login',views.login, name='login'),
    path('logout', views.logout,name='logout'),
    path('bussines_profile', views.bussines_profile,name='bussines_profile'),

]
