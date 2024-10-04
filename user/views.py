from rest_framework.response import Response
from rest_framework import status
from .models import User, Role
from .serializers import User_Serializer
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


# Create your views here.

# User Registration API
class RegisterUser(APIView):
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
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        return Response({
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
# To Update the user details.
class UpdateUser(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can update their info
    authentication_classes = [JWTAuthentication]  # Ensure JWT authentication is used
    # This is used to set the swagger UI. 
    @swagger_auto_schema(
        security=[{'bearerAuth': []}],  # This defines that this view requires JWT token
        operation_id="update_user",
        tags=["User"],
        request_body=UserUpdateSerializer,  # Expected input data
        responses={200: 'User updated successfully', 400: 'Bad Request'},
         manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)  # Fetch the user based on the primary key (pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Partial update
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)