from django.db import models
from user.models import User

# Create your models here.
class NGO(models.Model):
    ngo_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key referencing Users
    ngo_name = models.CharField(max_length=255)
    registration_no = models.CharField(max_length=100)
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField()
    website = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ngo_name