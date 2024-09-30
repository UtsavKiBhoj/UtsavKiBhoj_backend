from rest_framework import serializers
from .models import User, Role
from django.contrib.auth.hashers import make_password

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'role', 'name', 'email', 'password', 'phone', 'address', 'created_at', 'updated_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(User_Serializer, self).create(validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Name field cannot be empty.")
        if not data.get('email'):
            raise serializers.ValidationError("Email field cannot be empty.")
        if not data.get('password'):
            raise serializers.ValidationError("Password field cannot be empty.")
        return data
        

class Role_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'