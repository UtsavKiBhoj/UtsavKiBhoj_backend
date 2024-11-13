from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import EventSerializer, EventLocationSerializer
from .models import  Event, EventLocation
from food.models import FoodDetail 
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi 
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse


# Create a pagination class
class EventPagination(PageNumberPagination):
    page_size = 10  # Number of events per page
    page_size_query_param = 'page_size'
    max_page_size = 100

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
       print("request.data-------------------:", request.data)  # Log full request data for debugging
       data = request.data
       print("event_id--------------", data)
       event_id = data.get('event_id')
       print("event_id--------------", event_id)
       if event_id is None:
           return Response({"error": "Event ID is missing in the request data."}, status=status.HTTP_400_BAD_REQUEST)
    
       # Ensure the event_id is valid
       try:
           event = Event.objects.get(pk=event_id)  # Fetch the Event instance using event_id
       except Event.DoesNotExist:
           return Response({"error": "Event does not exist."}, status=status.HTTP_400_BAD_REQUEST)

       # Pass the Event instance directly to the serializer
       serializer = EventLocationSerializer(data=data)
       print("Data before saving:", data)

       if serializer.is_valid():
          try:
             # Save the serializer and pass the event instance separately
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
          except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET Event Details by ID API.
class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_id="Get_event_by_id",
        tags=["Event"],
        manual_parameters=[
            openapi.Parameter(
                'event_id',
                openapi.IN_PATH,
                description="ID of the event to retrieve",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: 'fetch Event successfully',
            404: 'Event not found'
        }
    )

    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EventDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_id="Get_event_by_id",
        tags=["Event"],
        manual_parameters=[
            openapi.Parameter(
                'event_id',
                openapi.IN_PATH,
                description="ID of the event to retrieve",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: 'fetch Event successfully',
            404: 'Event not found'
        }
    )
    def delete(self, request, event_id):
        try:
           event = Event.objects.get(event_id=event_id)
           event.eventlocation_set.all().delete()  # Delete related locations
           event.delete()
           return JsonResponse({"message": "Event deleted successfully!"}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found!"}, status=404)