from rest_framework import serializers
from .models import GeoLocation


class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if hasattr(instance, 'distance'):
            ret['distance'] = round(instance.distance.km, 2)

        return ret
