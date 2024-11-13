from django.urls import path
from .views import CreateEventView, CreateEventLocationView, EventListView, EventDetailView, EventDelete

urlpatterns = [
    path('Create-form/', CreateEventView.as_view(), name='event_details'),
    path('location-details/', CreateEventLocationView.as_view(), name='event_location_details'),
    path('list/', EventListView.as_view(), name='events_list'),
    path('detail/<int:event_id>', EventDetailView.as_view(), name='event_details'),
    path('delete/<int:event_id>', EventDelete.as_view(), name='event_delete'),
]
