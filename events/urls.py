from django.urls import path
from .views import CreateEventView, CreateEventLocationView, EventListView, EventDetailView

urlpatterns = [
    path('Create-form/', CreateEventView.as_view(), name='event_create'),
    path('location-form/', CreateEventLocationView.as_view(), name='event_location_create'),
    path('list/', EventListView.as_view(), name='events_list'),
    path('details/<int:event_id>', EventDetailView.as_view(), name='event_details'),
]
