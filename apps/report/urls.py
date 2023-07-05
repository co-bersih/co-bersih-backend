from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'reports', views.ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
