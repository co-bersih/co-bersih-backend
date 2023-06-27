from rest_framework.generics import CreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser

from .models import User
from .serializers import UserSerializer


# Create your views here.
class Register(CreateAPIView):
    queryset = User.objects.all()
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = UserSerializer
