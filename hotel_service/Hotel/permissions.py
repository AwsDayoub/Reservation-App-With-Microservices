from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
       if request.user.groups.filter(name='HotelManagers').exists():
            return True