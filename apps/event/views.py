import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from apps.report.models import Report
from apps.user.models import User
from apps.user.serializers import UserSerializer
from apps.utils.filters import GeoPointFilter
from .filters import EventFilter
from .models import Event, Payment
from .permissions import IsHostOrReadOnly, IsVerifiedEvent, IsStaff, IsFlipForBusiness
from .serializers import EventSerializer, EventDetailSerializer, StaffSerializer


# Create your views here.


@api_view(['GET'])
def hello_world(request):
    return Response({
        'message': 'hello world!'
    })


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsHostOrReadOnly]
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, GeoPointFilter]
    search_fields = ['name']
    filterset_class = EventFilter

    def perform_create(self, serializer):
        event = serializer.save(host=self.request.user)
        event.staffs.add(self.request.user)

        if 'report_ref_id' not in self.request.data:
            return

        try:
            report = Report.objects.get(pk=self.request.data['report_ref_id'])
            report.delete()
        except:
            return

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    @property
    def paginator(self):
        query_params = self.request.query_params
        if 'lon' in query_params and 'lat' in query_params \
                and ('min' in query_params or 'max' in query_params):
            return None
        return super().paginator

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            url_path='verify', url_name='verify')
    def verify_event(self, request, pk=None):
        event = self.get_object()
        event.is_verified = True
        event.save()

        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsVerifiedEvent],
            url_path='join', url_name='join')
    def join_event(self, request, pk=None):
        event = self.get_object()
        user = self.request.user

        if event.host == user:
            raise ValidationError({'id': 'you are the host of this event'}, code='user_is_event_host')
        elif user in event.staffs.all():
            raise ValidationError({'id': 'you are the staff of this event'}, code='user_is_event_staff')

        user.joined_events.add(event)
        return Response({'detail': 'user successfully joined'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsVerifiedEvent],
            url_path='leave', url_name='leave')
    def leave_event(self, request, pk=None):
        event = self.get_object()
        user = self.request.user
        user.joined_events.remove(event)
        return Response({'detail': 'user successfully left'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='staffs', url_name='staff-list')
    def add_staff(self, request, pk=None):
        event = self.get_object()
        staff_email = request.data.get('staff_email', '')

        serializer = StaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = User.objects.get(email=staff_email)

        # User can't be in joined_user and staffs at the same time
        if staff in event.joined_users.all():
            event.joined_users.remove(staff)

        event.staffs.add(staff)
        return Response({'detail': 'staff successfully updated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path=r'staffs/(?P<staff_email>[\w.@+-]+)', url_name='staff-detail')
    def delete_staff(self, request, pk=None, staff_email=None):
        event = self.get_object()

        serializer = StaffSerializer(data={'staff_email': staff_email})
        serializer.is_valid(raise_exception=True)
        staff = User.objects.get(email=staff_email)

        if event.host == staff:
            raise ValidationError({'email': 'you are the host of this event'}, code='user_is_event_host')

        event.staffs.remove(staff)
        return Response({'detail': 'staff successfully removed'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='accept-payment', url_name='accept-payment',
            permission_classes=[IsFlipForBusiness])
    def accept_payment(self, request):
        data = json.loads(request.data['data'])
        payment = Payment.objects.get(pk=int(data['bill_link_id']))
        event = payment.event

        if data['status'] == 'SUCCESSFUL':
            event.total_donation += data['amount']
            event.save()

        return Response(status=status.HTTP_200_OK)


class EventJoinedUserView(ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaff]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return User.objects.filter(joined_events=pk)
