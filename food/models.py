from django.db import models
from events.models import Event

# Create your models here.
class FoodDetail(models.Model):
    food_id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Foreign key referencing Events
    food_type = models.CharField(max_length=255)
    quantity = models.IntegerField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_type