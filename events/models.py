from django.db import models
from user.models import User

# Create your models here.
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key referencing Users
    event_name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name


class EventLocation(models.Model):
    location_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)  # Foreign key referencing Events
    location_name = models.CharField(max_length=255)
    address = models.TextField()
    pin_code = models.CharField(max_length=10, null=True, blank=True)  # New field for Pin Code
    landmark = models.CharField(max_length=255, null=True, blank=True)  # New field for Landmark
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location_name