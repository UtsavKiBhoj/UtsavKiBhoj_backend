from rest_framework import serializers
from .models import Claim

class Claim_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = '__all__'