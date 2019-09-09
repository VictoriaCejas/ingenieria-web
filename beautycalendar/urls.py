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
    url(r'products/$', views.mycontent_list, name='product_list'),
    url(r'products/create/$', views.mycontent_create, name='product_create'),
    url(r'products/(?P<pk>\d+)/update/$', views.mycontent_update, name='product_update'),
    url(r'products/(?P<pk>\d+)/delete/$', views.mycontent_delete, name='product_delete'),

    url(r'services/$', views.mycontent_list, name='service_list'),
    url(r'services/create/$', views.mycontent_create, name='service_create'),
    url(r'services/(?P<pk>\d+)/update/$', views.mycontent_update, name='service_update'),
    url(r'services/(?P<pk>\d+)/delete/$', views.mycontent_delete, name='service_delete'),

]