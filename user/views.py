from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import User, Role
from .serializers import User_Serializer,ForgotPasswordSerializer,ResetPasswordSerializer, LoginSerializer, UserUpdateSerializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
import os
from dotenv import load_dotenv

# Create your views here.
load_dotenv()

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
    
# Get/fetch User BY ID:
class getUserByID(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="get_user_by_id",
        tags=["User"],
        responses={
            200: openapi.Response('User retrieved successfully', User_Serializer),
            404: 'User not found'
        },
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, user_id):
        user = get_object_or_404(User, user_id=user_id)
        serializer = User_Serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
        
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
    # Allow any user to access this endpoint since it's for logout
    permission_classes = [AllowAny]

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
        refresh_token = request.data.get("refreshToken")
        
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token and blacklist it
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

        except TokenError:
            # If the token is invalid or expired, treat it as already logged out
            return Response({'message': 'Logout successful (token already invalid or expired)'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Catch any other unexpected errors
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_id="Forgot_Password",
        tags=["User"],
        responses={
            205: 'Forget password link sent to your mail successfully',
            400: 'Bad Request',
            401: 'Unauthorized'
        },
    )
    def post(self, request):
        # Validate the request data using ForgotPasswordSerializer
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            # Extract the email from the validated data
            email = serializer.validated_data.get('email')

            # Try to find the user with the provided email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'email': 'This email is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate the user ID and token
            #urlsafe_base64_encode: Encodes the user's primary key (user.pk) in a URL-safe base64 format (uid). This helps to ensure that the user ID is securely passed in the URL.
            # PasswordResetTokenGenerator().make_token(user): Generates a secure token that will be sent in the password reset link to the user’s email.
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            RESET_PASSWORD_ROUTE = os.getenv("RESET_PASSWORD_ROUTE")

            # Create the password reset link
            reset_link = f'{RESET_PASSWORD_ROUTE}/{uid}/{token}/'

            # Send the email with the reset link
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

            # If email is successfully sent, return a success message
            return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
        
        # Return errors if the serializer data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_id="Reset_Password",
        tags=["User"],
        responses={
            200: 'Password reset successfully',
            400: 'Invalid Token or Bad Request',
            401: 'Unauthorized'
        },
    )
    def post(self, request, uidb64, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the token is valid
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.password = make_password(serializer.validated_data['password'])
            user.save()

            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)