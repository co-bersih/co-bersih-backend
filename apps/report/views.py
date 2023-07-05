from rest_framework import viewsets
from rest_framework import permissions
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsReporterOrReadOnly


# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsReporterOrReadOnly]
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
