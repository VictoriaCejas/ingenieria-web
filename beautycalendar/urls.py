from django.urls import path, include
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.Home, name='home'),
    path('private_profile', views.PrivateProfile, name='private_profile'),
    path('private',views.Private, name='private'),
    path('public', views.Public, name='public'),

    
    #path('products', views.product_list, name='product_list'),
    #path('createproducts',views.product_create, name='product_create'),
    #path('product-create', view.product_create, name='product_create')
    #path('poducts/create'),views.product_create, name='product_create'),
    url(r'products/$', views.product_list, name='product_list'),
    url(r'products/create/$', views.product_create, name='product_create'),
    url(r'products/(?P<pk>\d+)/update/$', views.product_update, name='product_update'),
    url(r'products/(?P<pk>\d+)/delete/$', views.product_delete, name='product_delete'),

]