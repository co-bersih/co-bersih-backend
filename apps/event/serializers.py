from apps.user.models import User
from apps.user.serializers import UserSerializer
from rest_framework import serializers
from .models import Event, Payment


class EventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    host = UserSerializer(read_only=True)
    total_participant = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()
    account_number = serializers.CharField(write_only=True, required=False)
    bank_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Event
        fields = ['id', 'host', 'name', 'total_participant', 'description', 'preparation', 'image', 'image_url',
                  'latitude', 'longitude', 'start_date', 'end_date', 'is_verified', 'account_number', 'bank_code']

    def validate_account_number(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError('account number must be numeric', code='invalid_account_number')

        return value

    def validate(self, data):
        """
        Check that start_date is before end_date.
        """
        if data.get('start_date', self.instance.start_date if self.instance else None) > \
                data.get('end_date', self.instance.end_date if self.instance else None):
            raise serializers.ValidationError('end_date must occur after start_date', code='invalid_date')
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('image')

        if hasattr(instance, 'distance'):
            ret['distance'] = round(instance.distance.km, 2)

        return ret


class EventDetailSerializer(EventSerializer):
    staffs = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )
    supports = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    payment_url = serializers.ReadOnlyField()

    class Meta(EventSerializer.Meta):
        model = Event
        fields = EventSerializer.Meta.fields + ['staffs', 'supports', 'payment_url', 'total_donation']


class StaffSerializer(serializers.Serializer):
    staff_email = serializers.EmailField()

    def validate_staff_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('staff_email not found', code='invalid_id')
        return value


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
