from rest_framework import permissions
from .models import User

class IsVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(pk=request.user.pk)
        if user and user.email_verified:
            return True
        return False