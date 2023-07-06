from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import filters
from rest_framework.exceptions import ValidationError


class GeoPointFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        longitude = request.query_params.get('lon')
        latitude = request.query_params.get('lat')

        if not (longitude and latitude):
            return queryset

        try:
            current_point = Point(float(longitude), float(latitude), srid=4326)
            min_radius = request.query_params.get('min')
            max_radius = request.query_params.get('max')

            if min_radius and max_radius:
                min_radius = float(min_radius)
                max_radius = float(max_radius)

                if self.invalid_radius(min_radius, max_radius):
                    raise ValueError

                queryset = queryset.filter(point__distance_lte=(current_point, D(km=max_radius)),
                                           point__distance_gte=(current_point, D(km=min_radius)))
            elif max_radius:
                max_radius = float(max_radius)
                queryset = queryset.filter(point__distance_lte=(current_point, D(km=max_radius)))
            elif min_radius:
                min_radius = float(min_radius)
                queryset = queryset.filter(point__distance_gte=(current_point, D(km=min_radius)))

            return queryset
        except ValueError:
            raise ValidationError('invalid parameter', code='invalid_parameter')

    def invalid_radius(self, min_radius, max_radius):
        return min_radius < 0 or max_radius < 0 or max_radius < min_radius
