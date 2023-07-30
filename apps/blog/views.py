from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from .models import Blog
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes=[permissions.IsAdminUser]
    http_method_names = ['get', 'head', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @property
    def paginator(self):
        return super().paginator
