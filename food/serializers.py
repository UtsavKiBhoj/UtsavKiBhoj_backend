from rest_framework import serializers
from .models import FoodDetail

class FoodDetail_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FoodDetail
        fields = '__all__'