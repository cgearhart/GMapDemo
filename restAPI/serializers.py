"""
Automatically generate serializers from defined model schemas using
django-rest-framework.

http://django-rest-framework.org/api-guide/serializers.html#modelserializer

"""

from rest_framework import serializers
from restAPI.models import Station


class StationSerializer(serializers.ModelSerializer):
    # Field name must be equal to the `related_name` on the foreign key
    # associating the `Wine` model with the `Review` model.
    reviews = serializers.RelatedField(many=True)

    class Meta:
        model = Station
        fields = ('lat',
                  'lon',
                  'status'
                  )
        read_only_fields = ('id', )
