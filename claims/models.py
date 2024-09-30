from django.db import models
from ngos.models import NGO
from events.models import Event
from food.models import FoodDetail

# Create your models here.
class Claim(models.Model):
    claim_id = models.AutoField(primary_key=True)
    ngo = models.ForeignKey(NGO, on_delete=models.CASCADE)  # Foreign key referencing NGOs Detail
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # Foreign key referencing Events
    food = models.ForeignKey(FoodDetail, on_delete=models.CASCADE)  # Foreign key referencing Food Details
    claim_status = models.CharField(max_length=50)
    claimed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Claim {self.claim_id} - {self.claim_status}"