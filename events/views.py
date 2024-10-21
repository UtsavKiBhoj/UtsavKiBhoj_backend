from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import EventSerializer, EventLocationSerializer
from .models import  Event, EventLocation
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi 

# Create your views here.
class CreateEventView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="Create_Event",
        tags=["Event"],
        request_body=EventSerializer,  # Define the expected input
        responses={201: 'Event created successfully', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(organizer=request.user)  # Save the event with the logged-in user
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_id="Event_list",
        tags=["Event"],
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search events by name", type=openapi.TYPE_STRING)
        ],
        responses={200: EventSerializer(many=True), 400: 'Bad Request'}
    )
    def get(self, request):
        # Optionally filter events by search query
        search = request.GET.get('search')
        if search:
            events = Event.objects.filter(event_name__icontains=search)
        else:
            events = Event.objects.all()

        # Serialize the events and return the response
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
# Create Event Location View
class CreateEventLocationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id="Create_Event_Location",
        tags=["Event"],
        request_body=EventLocationSerializer,
        responses={201: 'Event Location created successfully', 400: 'Bad Request'}
    )
    def post(self, request):
        data = request.data
        # print("Event ID data----------", data)
        event_id = data.get('event')  
        # print("Event ID-----------", event_id)
        # Ensure the event_id is valid
        try:
            event = Event.objects.get(pk=event_id)  # Fetch the Event instance using event_id
        except Event.DoesNotExist:
            return Response({"error": "Event does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Pass the Event instance directly to the serializer
        serializer = EventLocationSerializer(data=data)  # Do not pop 'event' from the data
        print("Data before saving-----------------", data)

        if serializer.is_valid():
            try:
                # Save the serializer and pass the event instance separately
                serializer.save(event=event)  # Pass the event instance to the save method
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


