from rest_framework import serializers
from .models import Event, EventLocation
from django.utils import timezone
from user.serializers import User_Serializer

# EventLocationSerializer 
class EventLocationSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = EventLocation
        fields = ['location_id', 'location_name', 'address', 'pin_code', 'landmark', 'event']

    def create(self, validated_data):
        # No need to manually fetch `event` since `PrimaryKeyRelatedField` does it
        return EventLocation.objects.create(**validated_data)


# Event serializer
class EventSerializer(serializers.ModelSerializer):
    organizer = User_Serializer(read_only=True)
    location = EventLocationSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ['event_id', 'event_name', 'description', 'date', 'organizer', 'location']

    def validate_event_name(self, value):
        if not value:
            raise serializers.ValidationError("Event name is required.")
        return value

    def validate_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past.")
        return value
    
    
    
class EventUpdateSerializer(serializers.ModelSerializer):
    location = serializers.CharField()
    email = serializers.EmailField(source='organizer.email', read_only=True)
    phone = serializers.CharField(source='organizer.phone', read_only=True)
    name = serializers.CharField(source='organizer.name', read_only=True)

    class Meta:
        model = Event
        fields = ['event_id', 'event_name', 'description', 'date', 'location', 
                  'email', 'phone', 'name']
    
    def update(self, instance, validated_data):
        # Update Event fields
        instance.event_name = validated_data.get('event_name', instance.event_name)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.save()
        
        # Update related EventLocation
        location_data = validated_data.get('location', {})
        if location_data:
            instance.location_name = location_data  # Set location to string
            instance.save()
        else:
            # Create a new location
            EventLocation.objects.create(event=instance, **location_data)
            
        organizer_data = validated_data.get('organizer', {})
        if organizer_data:
            instance.organizer.name = organizer_data.get('name', instance.organizer.name)
            instance.organizer.phone = organizer_data.get('phone', instance.organizer.phone)
            instance.organizer.save()

        return instance
