from rest_framework import serializers
from .models import User, Role
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

# User Registration Serializer 
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
        
# User Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password.")

        # Check password
        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data