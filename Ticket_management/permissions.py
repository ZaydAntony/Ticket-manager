from rest_framework.permissions import BasePermission


class IsTechnician(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Allow admins
        if user.is_staff:
            return True

        # Allow technicians (assuming role field)
        return user.role == "Technician"
