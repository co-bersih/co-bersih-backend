from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'events', views.EventViewSet, basename='event')

urlpatterns = [
    path("hello-world/", views.hello_world, name='hello-world'),
    path('', include(router.urls)),
    path('events/<uuid:pk>/joined-users/', views.EventJoinedUserView.as_view(), name='event-joined-user-list'),
]
