from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from apps.utils.filters import GeoPointFilter
from .models import Report
from .permissions import IsReporterOrReadOnly
from .serializers import ReportSerializer


# Create your views here.
class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsReporterOrReadOnly]
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = [GeoPointFilter, filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @property
    def paginator(self):
        if 'lon' in self.request.query_params and 'lat' in self.request.query_params:
            return None
        return super().paginator
