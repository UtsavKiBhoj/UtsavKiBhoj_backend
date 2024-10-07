from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import User, Role
from .serializers import User_Serializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserUpdateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import jwt, os, datetime
from rest_framework import generics

# Create your views here.


# User Registration API
class RegisterUser(APIView):
    permission_classes = [AllowAny]  # Allow any user to register without authentication
    renderer_classes = [JSONRenderer]
    @swagger_auto_schema(
        operation_id="register_user", 
        tags=["User"],
        request_body=User_Serializer,  # Define the expected input
        responses={201: User_Serializer, 400: 'Bad Request'}  # Define the possible responses
    )
    def post(self, request):
        serializer = User_Serializer(data=request.data)
        
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
        
        
# User Login API
class LoginUser(APIView):
    permission_classes = [AllowAny]  # Allow any user to register without authentication

    @swagger_auto_schema(
        operation_id="login_user",
        tags=["User"],
        request_body=LoginSerializer,  # Define the expected input
        responses={200: 'JWT tokens', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT token
            # payload = {
            #     'id': user.user_id,  
            #     'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)  # Set expiration time
            # }
            # Ensure you have set this in your Django settings
            # secret_key = os.getenv("SECRET_KEY")
            # print("bdwbewbfee----secret_keysecret_key------------",secret_key)
            # jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')

            # Generate Refresh and Access tokens using Simple JWT
            # refresh = RefreshToken.for_user(user)

            return Response({
                'message': f'{"Welcome", user.name, 'Login successful'}',
                # 'refresh': str(refresh),
                # 'access': str(refresh.access_token),
                # 'jwt': jwt_token  # Include your generated JWT token in the response
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
class UserListView(generics.ListAPIView):
    @swagger_auto_schema(
        operation_id="list_users",
        tags=["User"],
        responses={
            200: 'Users List view',
            400: 'Bad Request',
            404: 'User not found'
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve list of users"""
        return super().get(request, *args, **kwargs)

    queryset = User.objects.all()
    serializer_class = User_Serializer
        
        
# To Update the user details.
class UpdateUser(APIView):
    @swagger_auto_schema(
        operation_id="update_user",
        tags=["User"],
        request_body=UserUpdateSerializer,  # Expected input data format
        responses={
            200: 'User updated successfully', 
            400: 'Bad Request',
            404: 'User not found'
        },
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def put(self, request, pk):
        # Fetch the user based on the primary key (pk)
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Perform a partial update of the user's data
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save the updated user data
            return Response({
                'message': 'User updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        # Return validation errors if any
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteUser(APIView):
    @swagger_auto_schema(
        operation_id="delete_user",
        tags=["User"],
        request_body=LoginSerializer,  # Define the expected input
        responses={
            200: "User deleted successfully",
            400: "Bad Request",
            404: "User not found",
        })
    def delete(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)