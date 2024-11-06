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
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())
    class Meta:
        model = EventLocation
        fields = ['location_name', 'address', 'pin_code', 'landmark', 'event'] 

    # def validate_event(self, value):
    #     # Ensure the `event` field is an integer (event_id), not an Event object
    #     if isinstance(value, Event):
    #         value = value.event_id  # Use the ID of the event if an object is passed
    def validate_event(self, value):
        # Validate that the provided event exists
        if not Event.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Event does not exist.")
        return value
    
    def create(self, validated_data):
        event_id = validated_data.pop('event')  # Get event_id from validated data
        event = Event.objects.get(pk=event_id)  # Fetch the Event instance using event_id
        
        # Create an EventLocation instance with the event
        event_location = EventLocation.objects.create(event=event, **validated_data)
        return event_location