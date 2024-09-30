from rest_framework import serializers
from .models import Feedback

class Feedback_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'