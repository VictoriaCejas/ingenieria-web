from rest_framework import serializers
from .models import UserDates, ContentUsers


class servicesSerializer(serializers.ModelSerializer):

    class Meta:
        model= ContentUsers
        fields=('title',)

class eventsSerializer(serializers.ModelSerializer):
    title= serializers.StringRelatedField(source='service')
    start= serializers.ReadOnlyField(source='init_time')
    end= serializers.ReadOnlyField(source='finish_time')
    class Meta:
        model= UserDates
        fields=('title','start','end')

