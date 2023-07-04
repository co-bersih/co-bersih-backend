from apps.user.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Event
from .permissions import IsHostOrReadOnly, IsVerifiedEvent
from .serializers import EventSerializer, EventDetailSerializer, StaffSerializer


# Create your views here.


@api_view(['GET'])
def hello_world(request):
    return Response({
        'message': 'hello world!'
    })


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsHostOrReadOnly]
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['is_verified']

    def perform_create(self, serializer):
        event = serializer.save(host=self.request.user)
        event.staffs.add(self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        is_verified = self.request.query_params.get('is_verified')
        if self.action == 'list' and is_verified is None:
            queryset = queryset.filter(is_verified=True)
        return queryset

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
        staff_id = request.data.get('staff_id', '')

        serializer = StaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = User.objects.get(pk=staff_id)

        if staff in event.joined_users.all():
            raise ValidationError({'id': 'you already joined this event as user'}, code='user_already_joined_event')

        event.staffs.add(staff)
        return Response({'detail': 'staff successfully updated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='staffs/(?P<staff_pk>[^/.]+)', url_name='staff-detail')
    def delete_staff(self, request, pk=None, staff_pk=None):
        event = self.get_object()

        serializer = StaffSerializer(data={'staff_id': staff_pk})
        serializer.is_valid(raise_exception=True)
        staff = User.objects.get(pk=staff_pk)

        if event.host == staff:
            raise ValidationError({'id': 'you are the host of this event'}, code='user_is_event_host')

        event.staffs.remove(staff)
        return Response({'detail': 'staff successfully removed'}, status=status.HTTP_200_OK)
