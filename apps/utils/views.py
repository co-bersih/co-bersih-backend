from rest_framework import generics

from .filters import GeoPointFilter
from .models import GeoLocation
from .serializer import GeoLocationSerializer


# Create your views here.
class GeoView(generics.ListAPIView):
    queryset = GeoLocation.objects.all()
    serializer_class = GeoLocationSerializer
    filter_backends = [GeoPointFilter]
