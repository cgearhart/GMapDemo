"""
Automatically generate serializers from defined model schemas using
django-rest-framework.

http://django-rest-framework.org/api-guide/serializers.html#modelserializer

"""

from rest_framework import serializers
from restAPI.models import Station


class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ('lat',
                  'lon',
                  'stat'
                  )
        read_only_fields = ('id', )
