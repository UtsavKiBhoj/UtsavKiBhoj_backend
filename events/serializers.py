from rest_framework import serializers
from .models import Event, EventLocation

class Event_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        

class EventLocation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = '__all__'