from rest_framework import permissions


class IsHostOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.host == request.user


class IsVerifiedEvent(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_verified
