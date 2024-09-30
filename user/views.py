from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import User, Role
from .serializers import UserSerializer
from rest_framework.views import APIView


# Create your views here.
class RegisterUser(APIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        # Check if the data is valid, return errors if any
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User registered successfully!',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        # Return validation errors
        return Response({
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)