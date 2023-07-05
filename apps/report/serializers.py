from rest_framework import serializers
from .models import Report
from apps.user.serializers import UserSerializer


class ReportSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()
    reporter = UserSerializer(read_only=True)
    reported_date = serializers.ReadOnlyField()

    class Meta:
        model = Report
        fields = ['id', 'title', 'image', 'image_url', 'reporter', 'reported_date', 'description',
                  'latitude', 'longitude']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('image')

        return ret
