from rest_framework import serializers
from .models import User, Role
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


# User Registration Serializer 
class User_Serializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = User
        fields = ['user_id', 'role', 'name', 'email', 'password', 'phone', 'address', 'created_at', 'updated_at', "is_active"]
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
        
# User Role Serializer.
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
    
# user update serializer
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Specify fields that can be updated
        fields = ['name', 'email', 'phone', 'address']  
        
        
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_password(self, value):
        # Add custom password validation if needed
        # if len(value) < 8:
        #     raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value