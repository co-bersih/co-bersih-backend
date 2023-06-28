from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import permissions

from .models import User
from .serializers import UserSerializer
from .permissions import IsCurrentUserOrReadOnly


# Create your views here.
class Register(CreateAPIView):
    queryset = User.objects.all()
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = UserSerializer


class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsCurrentUserOrReadOnly]


class CurrentUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return current user details
        """
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)
