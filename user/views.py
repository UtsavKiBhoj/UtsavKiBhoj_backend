from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
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
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

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
    # Swagger Annotation for the UI in swaggger
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
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'message': f'{"Welcome", user.name, 'Login successful'}',
                'access_token': access_token,
                'refresh_token': refresh_token
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
        
#  Users List View
class UserListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
        users = User.objects.all()  # Use your custom User model
        serializer = User_Serializer(users, many=True)
        return Response(serializer.data)
        
        
# To Update the user details.
class UpdateUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
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
    
    
# Delete Users View.
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
        
        
class LogoutUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="logout_user",
        tags=["User"],
        responses={
            205: 'Logout successful',
            400: 'Bad Request',
            401: 'Unauthorized'
        },
    )
    def post(self, request):
        try:
            # Extract the refresh token from request data
            refresh_token = request.data["refreshToken"]
            print("refresh_token--------refresh_token----", refresh_token)

            # Decode and validate the token using RefreshToken
            token = RefreshToken(refresh_token)
            
            # Blacklist the token
            try:
                # Check if the token is already blacklisted
                BlacklistedToken.objects.get(token=OutstandingToken.objects.get(token=token))
                return Response({'error': 'Token already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)
            except BlacklistedToken.DoesNotExist:
                # If not already blacklisted, blacklist it
                token.blacklist()
                return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

        except KeyError:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        except OutstandingToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError:
            return Response({'error': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)