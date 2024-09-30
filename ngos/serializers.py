from rest_framework import serializers
from .models import NGO

class NGO_Serializer(serializers.ModelSerializer):
    class Meta:
        model = NGO
        fields = '__all__'