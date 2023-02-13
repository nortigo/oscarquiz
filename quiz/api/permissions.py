from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminHasWritePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            return request.user.is_staff
        return False
