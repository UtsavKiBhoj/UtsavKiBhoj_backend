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
    # Use `event` instead of `event_id` since it's a ForeignKey
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = EventLocation
        fields = ['location_name', 'address', 'pin_code', 'landmark', 'event']

    def create(self, validated_data):
        # No need to manually fetch `event` since `PrimaryKeyRelatedField` does it
        return EventLocation.objects.create(**validated_data)