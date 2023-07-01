from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions

from .models import Event
from .serializers import EventSerializer, EventDetailSerializer, AddStaffSerializer
from .permissions import IsHostOrReadOnly

from apps.user.models import User

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

    def perform_create(self, serializer):
        event = serializer.save(host=self.request.user)
        event.staffs.add(self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated],
            url_path='join', url_name='join')
    def join_event(self, request, pk=None):
        event = self.get_object()
        user = self.request.user

        if event.host == user:
            return Response({'detail': 'you are the host of this event'}, status=status.HTTP_400_BAD_REQUEST)
        elif user in event.staffs.all():
            return Response({'detail': 'you are the staff of this event'}, status=status.HTTP_400_BAD_REQUEST)

        user.joined_events.add(event)
        return Response({'detail': 'user successfully joined'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='staffs', url_name='staffs')
    def add_staff(self, request, pk=None):
        event = self.get_object()
        staff_id = request.data.get('staff_id', '')

        serializer = AddStaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = User.objects.get(pk=staff_id)

        if staff in event.joined_users.all():
            return Response({'detail': 'you already joined this event as user'}, status=status.HTTP_400_BAD_REQUEST)

        event.staffs.add(staff)
        return Response({'detail': 'staff successfully updated'}, status=status.HTTP_200_OK)
