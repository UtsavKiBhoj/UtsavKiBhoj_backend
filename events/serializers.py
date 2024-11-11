from rest_framework import serializers
from .models import Event, EventLocation
from django.utils import timezone
from user.serializers import User_Serializer



class EventSerializer(serializers.ModelSerializer):
    organizer = User_Serializer(read_only=True)
    class Meta:
        model = Event
        fields = ['event_id', 'event_name', 'description', 'date', 'organizer']

    def validate_event_name(self, value):
        if not value:
            raise serializers.ValidationError("Event name is required.")
        return value

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past.")
        return value

# EventLocationSerializer 
class EventLocationSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = EventLocation
        fields = ['location_name', 'address', 'pin_code', 'landmark', 'event_id']

    def create(self, validated_data):
        # Pop the event_id from validated_data
        event_id = validated_data.pop('event_id')
        
        # Fetch the Event instance
        event = Event.objects.get(pk=event_id)
        
        # Pass the event instance to create EventLocation
        event_location = EventLocation.objects.create(event_id=event.event_id, **validated_data)
        return event_location