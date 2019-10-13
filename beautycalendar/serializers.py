from rest_framework import serializers
from .models import UserDates, ContentUsers, WorkingHoursSalons, BeautySalons


class servicesSerializer(serializers.ModelSerializer):

    class Meta:
        model= ContentUsers
        fields=('title',)

class eventsSerializer(serializers.ModelSerializer):
    id= serializers.ReadOnlyField(source='pk')
    title= serializers.StringRelatedField(source='service')
    start= serializers.ReadOnlyField(source='init_time')
    end= serializers.ReadOnlyField(source='finish_time')
    class Meta:
        model= UserDates
        fields=('id','title','start','end')


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