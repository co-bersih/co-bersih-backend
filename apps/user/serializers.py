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

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        return instance

    def validate_email(self, value):
        if self.instance and value != self.instance.email:
            raise serializers.ValidationError("email is immutable once set.")
        return value

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop('profile_image')

        return ret
