from rest_framework import permissions
from django.contrib.auth.models import User


class IsSenderOrReceiver(permissions.BasePermission):
    """
    Custom permission to allow only sender and receiver reach the message.
    """
    def has_object_permission(self, request, view, obj):
        user = User.objects.get(username=request.user.username)
        return obj.sender == user or obj.receiver == user
