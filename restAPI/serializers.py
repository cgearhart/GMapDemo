"""
Automatically generate serializers from defined model schemas using
django-rest-framework.

http://django-rest-framework.org/api-guide/serializers.html#modelserializer

"""

from rest_framework import serializers
from restAPI.models import Station


class StationSerializer(serializers.ModelSerializer):

    # simulated station state; disable this line (and enable code in
    # models.py) to handle `stat` as a model field in order to use the
    # API for health monitoring.
    stat = serializers.CharField(source='get_stat', read_only=True)

    class Meta:
        model = Station
        fields = ('lat',
                  'lon',
                  'stat',
                  )
        read_only_fields = ('id', )
