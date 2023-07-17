from rest_framework import permissions
from apps.event.models import Event
from django.shortcuts import get_object_or_404


class IsHostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.host == request.user


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        event_pk = view.kwargs['pk']
        event = get_object_or_404(Event, pk=event_pk)
        return request.user in event.staffs.all()


class IsVerifiedEvent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_verified
