from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls import handler404

urlpatterns = [
    path('', views.Home, name='home'),
    url(r'^accounts/password/change/$', views.password_change, name='password_change'),

    url(r'^accounts/', include('allauth.urls')),

    path('private_profile', views.PrivateProfile, name='private_profile'),
    path('private',views.Private, name='private'),
    path('public', views.Public, name='public'),

    url(r'filter_professional/(?P<pk>\d+)/$', views.filter_professional, name="filter_professional"),

    
    #path('products', views.product_list, name='product_list'),
    #path('createproducts',views.product_create, name='product_create'),
    #path('product-create', view.product_create, name='product_create')
    #path('poducts/create'),views.product_create, name='product_create'),
    url(r'products/$', views.mycontent_list, name='product_list'),
    url(r'products/create/$', views.mycontent_create, name='product_create'),
    url(r'products/(?P<pk>\d+)/update/$', views.mycontent_update, name='product_update'),
    url(r'products/(?P<pk>\d+)/delete/$', views.mycontent_delete, name='product_delete'),
    url(r'products/(?P<pk>\d+)/pause/$', views.mycontent_pause, name='product_pause'),


    url(r'services/$', views.mycontent_list, name='service_list'),
    url(r'services/create/$', views.mycontent_create, name='service_create'),
    url(r'services/(?P<pk>\d+)/update/$', views.mycontent_update, name='service_update'),
    url(r'services/(?P<pk>\d+)/delete/$', views.mycontent_delete, name='service_delete'),
    url(r'services/(?P<pk>\d+)/pause/$', views.mycontent_pause, name='service_pause'),

    url(r'empleoyees/$', views.mycontent_list, name='empleoyee_list'),
    url(r'empleoyees/create/$', views.mycontent_create, name='empleoyee_create'),
    url(r'empleoyees/(?P<pk>\d+)/update/$', views.mycontent_update, name='empleoyee_update'),
    url(r'empleoyees/(?P<pk>\d+)/delete/$', views.mycontent_delete, name='empleoyee_delete'),
    url(r'empleoyees/(?P<pk>\d+)/pause/$', views.mycontent_pause, name='empleoyee_pause'),

    url(r'profile/(?P<pk>\d+)/update/avatar/$', views.avatar_update, name='avatar_update'),
    url(r'profile/(?P<pk>\d+)/update/front/$', views.front_update, name='front_update'),
    url(r'profile/(?P<pk>\d+)/update/bio/$', views.bio_update, name='bio_update'),

    url(r'privacy-policy-facebook/$',views.facebookprivacy, name= 'facebook-privacy'),

    url(r'profile/(?P<email>[\w.@+-]+)/$', views.PublicProfile, name= 'public_profile'),

    url(r'calendar/(?P<pk>\d+)/$',views.Calendar, name='calendar'),
    url(r'calendar/(?P<pk>\d+)/confirm/$', views.confirmarTurno, name='confirm-date'),
    url(r'calendar/(?P<pk>\d+)/empleoyee_calendar/$', views.getCalendarBussines, name='empleoyee_calendar'),
    url(r'calendar/client',views.getCalendarClient, name='client_calendar'),
    
    url(r'publications/$', views.listPublication, name='publications'),
    url(r'publications/create/$', views.createPublication, name='publications_create'),
    url(r'publications/(?P<pk>\d+)/$', views.getPublication, name='publication_get'),
    url(r'publications/(?P<pk>\d+)/comment/$', views.getPublication, name='save-comment'),

    # url(r'events/$',views.getEvents, name='events'),
    url(r'events/(?P<pk>\d+)/empleoyee', views.getEventsBussines, name='events_bussines'),
    url(r'events/client',views.getEventsClient, name='events_client'),
    
    url(r'bio/daysandhours', views.get_HoursandDays, name='wkhours'),
    url(r'bio/items',views.get_items, name='get_items')
]
handler404 = views.mi_error_404