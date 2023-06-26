from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializer


# Create your views here.
class Register(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
