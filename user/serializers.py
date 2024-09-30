from rest_framework import serializers
from .models import User, Role

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        

class Role_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'