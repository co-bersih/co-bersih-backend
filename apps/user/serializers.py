from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    date_joined = serializers.ReadOnlyField()
    profile_image_url = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'date_joined', 'bio', 'profile_image', 'profile_image_url']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate_email(self, value):
        if self.instance and value != self.instance.email:
            raise serializers.ValidationError('email is immutable once set.')
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('profile_image')

        return ret


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    def validate_old_password(self, value):
        user = self.instance
        if not user.check_password(value):
            raise serializers.ValidationError(
                'Your old password was entered incorrectly. Please enter it again.',
                code='invalid_password')
        return value

    def validate_new_password(self, value):
        user = self.instance
        password_validation.validate_password(value, user)
        return value

    def update(self, instance, validated_data):
        user = self.instance
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user
