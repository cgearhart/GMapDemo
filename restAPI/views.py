
from rest_framework import generics
from rest_framework import permissions

from rest_framework.authentication import SessionAuthentication

from restAPI.models import Station
from restAPI.serializers import StationSerializer

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
        fields = ('status',
                  )


class StationList(generics.ListCreateAPIView):
    """
    Generic list view.
    """
    # SessionAuthentication should be removed for production version
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsStaffOrReadOnly,)  # must be staff user to add wine
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_class = StationFilter
