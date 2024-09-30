from django.db import models
from user.models import User
from events.models import Event

# Create your models here.
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key referencing Users
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Foreign key referencing Events
    rating = models.IntegerField()
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.feedback_id} by {self.user.name}"
