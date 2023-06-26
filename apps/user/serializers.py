from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'name', 'date_joined', 'bio']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
