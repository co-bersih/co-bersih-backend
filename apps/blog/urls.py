from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'blogs', views.BlogViewSet, basename='blog')

urlpatterns = [
    path('', include(router.urls)),
]
