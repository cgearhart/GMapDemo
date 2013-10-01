
from rest_framework import generics
from rest_framework import permissions

from restAPI.models import Station, Event
from restAPI.serializers import StationSerializer, EventSerializer

import django_filters


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow editing objects by staff users only.
    Assumes the `request.user` instance has an `is_staff` attribute.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff


class StationFilter(django_filters.FilterSet):
    """
    Filter class for to allow sorting & grouping results by model fields.
    """

    status = django_filters.MultipleChoiceFilter()

    class Meta:
        model = Station
        order_by = True


class StationList(generics.ListCreateAPIView):
    """
    Generic list view.
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_class = StationFilter


class EventFilter(django_filters.FilterSet):
    """
    Filter class for to allow sorting & grouping results by model fields.
    """

    class Meta:
        model = Event
        order_by = True
        fields = ("station_id",
                  )


class EventList(generics.ListCreateAPIView):
    """
    Generic list view.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_class = EventFilter
