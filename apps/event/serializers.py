from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from .models import Event
from apps.user.serializers import UserSerializer
from apps.user.models import User


class EventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    host = UserSerializer(read_only=True)
    total_participant = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'host', 'name', 'total_participant', 'description', 'preparation', 'image', 'image_url',
                  'latitude', 'longitude', 'start_date', 'end_date']

    def validate(self, data):
        """
        Check that start_date is before end_date.
        """
        if data.get('start_date', self.instance.start_date if self.instance else None) > \
                data.get('end_date', self.instance.end_date if self.instance else None):
            raise serializers.ValidationError({'invalid_date': ErrorDetail('end_date must occur after start_date')})
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('image')

        return ret


class EventDetailSerializer(EventSerializer):
    staffs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    supports = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(EventSerializer.Meta):
        model = Event
        fields = EventSerializer.Meta.fields + ['staffs', 'supports']


class AddStaffSerializer(serializers.Serializer):
    staff_id = serializers.UUIDField()

    def validate_staff_id(self, value):
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(ErrorDetail('staff_id not found'))
        return value
