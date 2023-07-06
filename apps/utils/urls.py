from django.urls import path

from . import views

urlpatterns = [
    path('locations/', views.GeoView.as_view(), name='location-list'),
]
