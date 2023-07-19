from apps.event.models import Event
from apps.event.serializers import EventSerializer
from apps.report.models import Report
from apps.report.serializers import ReportSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .permissions import IsCurrentUserOrReadOnly
from .serializers import UserSerializer, CurrentUserSerializer, ChangePasswordSerializer


# Create your views here.
class Register(CreateAPIView):
    queryset = User.objects.all()
    parser_classes = [FormParser, MultiPartParser]
    serializer_class = UserSerializer
    throttle_scope = 'register'


class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsCurrentUserOrReadOnly]
    http_method_names = ['get', 'head', 'patch']

    def partial_update(self, request, *args, **kwargs):
        request_keys = request.data.keys()
        if 'old_password' in request_keys or 'new_password' in request_keys:
            user = self.get_object()
            serializer = ChangePasswordSerializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        elif 'password' in request_keys:
            raise ValidationError('User is not allowed to change password'
                                  'without providing old_password and new_password', code='password')

        return super().partial_update(request, *args, **kwargs)


class CurrentUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return current user details
        """
        serializer = CurrentUserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserEventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Event.objects.filter(joined_users=pk)


class UserEventDetailView(RetrieveAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = 'event_pk'

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Event.objects.filter(joined_users=pk)


class UserEventStaffView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Event.objects.filter(staffs=pk)


class UserReportView(ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Report.objects.filter(reporter=pk)
