from rest_framework import serializers
from .models import UserDates, ContentUsers, WorkingHoursSalons, BeautySalons, CommentsPublications, Users
from allauth.socialaccount.models import SocialToken


"""Usados por beautycalendar"""
class servicesSerializer(serializers.ModelSerializer):

    class Meta:
        model= ContentUsers
        fields=('title',)

class userEventSerializer(serializers.ModelSerializer):
    salon=serializers.ReadOnlyField()
    class Meta:
        model=Users
        fields=['name_salon','salon']
        
class eventsSerializer(serializers.ModelSerializer):
    id= serializers.ReadOnlyField(source='pk')
    title= serializers.StringRelatedField(source='service')
    start= serializers.ReadOnlyField(source='init_time')
    end= serializers.ReadOnlyField(source='finish_time')
    class Meta:
        model= UserDates
        fields=('id','title','start','end','client','salon','empleoyee')


class wkHoursSerializer(serializers.ModelSerializer):
    itime=serializers.DateTimeField(format="%H:%M",source='init_time')
    ftime=serializers.DateTimeField(format="%H:%M",source="finish_time")
    class Meta:
        model= WorkingHoursSalons
        fields= ['init_date','finish_date','itime','ftime']

        
class itemsSelectedSerialezer(serializers.ModelSerializer):
    class Meta:
        model= BeautySalons
        fields=['items']
        

"""Usados en API"""
class serviceSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContentUsers
        fields=['user','title','price','attention_time']

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContentUsers
        fields=['user','title','price']
        
class bussineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=['first_name','last_name','name_salon','description']

class tokenSerializer(serializers.ModelSerializer):
    class Meta:
        model=SocialToken
        fields= ['token']

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields='__all__'