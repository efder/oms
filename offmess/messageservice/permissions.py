from rest_framework import permissions
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class IsSenderOrReceiver(permissions.BasePermission):
    """
    Custom permission to allow only sender and receiver reach the message.
    """
    def has_object_permission(self, request, view, obj):
        try:
            user = User.objects.get(username=request.user.username)
        except ObjectDoesNotExist:
            return false
        return obj.sender == user or obj.receiver == user
        