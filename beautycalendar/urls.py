from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf.urls import handler404
from rest_framework import routers
from . import apiViews
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView

router= routers.DefaultRouter()
router.register(r'users',apiViews.UserView,base_name='users')
# router.register(r'services',apiViews.ServicesView)
# router.register(r'services',apiViews.servicesViewSet)
# router.register(r'services', apiViews.servicesViewSet, basename='services')
urlpatterns = [
    
    path('api/', include(router.urls)),
    
    path('api/token-auth/',obtain_auth_token,name='api_token_auth'),
    
    path('api/rest-auth/', include('rest_auth.urls')),
    
    path('api/rest-auth/facebook', apiViews.FacebookLogin.as_view(), name='fb-login'),

    path('api/rest-auth/google',apiViews.GoogleLogin.as_view(), name='google-login'),
    
    path('api/services/',apiViews.ServicesView.as_view(),name='services'),
    
    url(r'api/services/(?P<email>[\w.@+-]+)/',apiViews.ServiceList.as_view(),name='services-bussines'),
    
    url(r'api/dates/get',apiViews.DatesClientView.as_view(),name='dates-client'),
    url(r'api/dates/post',apiViews.DatesClientView.as_view(),name='post-dates-client'),
    path('api/token/',apiViews.tokenAppView.as_view(),name='token-app'),
    
    # url(r'api/users/',apiViews.UserView.as_view({'get':'list'}),name='users'),
    # url(r'api/users/(?P<email>[\w.@+-]+)/', apiViews.UserView.as_view({'get':'one'}),name='user'),
    # url('api/services/(?P<email>.+)/$', apiViews.ServiceList.as_view()),

    path('', views.Home, name='home'),
    
    url(r'^accounts/password/change/$', views.password_change, name='password_change'),

    url(r'^accounts/', include('allauth.urls')),

    path('private_profile', views.PrivateProfile, name='private_profile'),

    url(r'filter_professional/(?P<pk>\d+)/$', views.filter_professional, name="filter_professional"),


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

    url(r'draws/$', views.mycontent_list, name='draw_list'),
    url(r'draws/create/$', views.mycontent_create, name='draw_create'),
    url(r'draws/(?P<pk>\d+)/delete/$', views.mycontent_delete, name='draw_delete'),
    url(r'draw/(?P<pk>\d+)/$', views.getDraw, name='get_draw'),
    url(r'draw-client/$', views.getDrawClient, name='draws_client'),
    url(r'draw-insc/(?P<pk>\d+)/$', views.inscriptionDraw, name='inscription_draw'),
    url(r'draw-participant/(?P<pk>\d+)/$',views.getParticipants, name='draw_participants'),
    
    url(r'profile/(?P<pk>\d+)/update/avatar/$', views.avatar_update, name='avatar_update'),
    url(r'profile/(?P<pk>\d+)/update/front/$', views.front_update, name='front_update'),
    url(r'profile/(?P<pk>\d+)/update/bio/$', views.bio_update, name='bio_update'),
    
    url(r'profile/(?P<email>[\w.@+-]+)/$', views.PublicProfile, name= 'public_profile'),
    url(r'profile/(?P<email>[\w.@+-]+)/report/$',views.reporter, name='report'),

    url(r'calendar/(?P<pk>\d+)/$',views.Calendar, name='calendar'),
    url(r'calendar/(?P<pk>\d+)/confirm/$', views.confirmarTurno, name='confirm-date'),
    url(r'calendar/(?P<pk>\d+)/empleoyee_calendar/$', views.getCalendarBussines, name='empleoyee_calendar'),
    url(r'calendar/client',views.getCalendarClient, name='client_calendar'),
    
    url(r'publications/private/(?P<email>[\w.@+-]+)/$', views.listPublication, name='publications-private'),
    url(r'publications/client/(?P<email>[\w.@+-]+)/$', views.listPublication, name='publications-client'),
    url(r'publications/create/$', views.createPublication, name='publications_create'),
    url(r'publications/(?P<pk>\d+)/$', views.getPublication, name='publication_get'),
    url(r'publications/(?P<pk>\d+)/comment/$', views.saveComment, name='save_comment'),
    url(r'publication-delete/(?P<pk>\d+)',views.DeletePublication, name='publication_delete'),

    # url(r'events/$',views.getEvents, name='events'),
    url(r'events/(?P<pk>\d+)/empleoyee', views.getEventsBussines, name='events_bussines'),
    url(r'events/client',views.getEventsClient, name='events_client'),
    
    url(r'bio/daysandhours', views.get_HoursandDays, name='wkhours'),
    url(r'bio/items',views.get_items, name='get_items'),
    
    url(r'privacy-policy-facebook/$',views.facebookprivacy, name= 'facebook-privacy'),

    url(r'block-user/(?P<email>[\w.@+-]+)/(?P<pk>\d+)', views.StateUser, name="blockuser"),
    url(r'block-user-user/(?P<email>[\w.@+-]+)/', views.StateUser, name="blockuser-user"),
    url(r'report-delete/(?P<pk>\d+)/$',views.DeleteReport, name="report-delete"),
    url(r'reports/',views.ListReports, name='reports'),
    url(r'users-locked/', views.ListUsersLockes, name='users-locked'),
    url(r'delete-event/(?P<pk>\d+)',views.DeleteEvet, name='delete-event'),
    
    url(r'like/(?P<pk>\d+)',views.Like,name='like'),
    url(r'dislike/(?P<pk>\d+)',views.Like,name='dislike'),
    url(r'totalLikes/(?P<pk>\d+)', views.TotalLikes, name='totalLikes'),

    url(r'^search/', include('haystack.urls')),
    url(r'^search/autocomplete',views.autocomplete, name='autocomplete'),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'))
    

]
handler404 = views.mi_error_404