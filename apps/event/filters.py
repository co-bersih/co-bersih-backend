from django_filters import rest_framework as filters
from .models import Event


class EventFilter(filters.FilterSet):
    class Meta:
        model = Event
        fields = {
            'is_verified': ['exact'],
            'start_date': ['exact', 'lte', 'lt', 'gte', 'gt'],
            'end_date': ['exact', 'lte', 'lt', 'gte', 'gt'],
        }
