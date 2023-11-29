from rest_framework.permissions import BasePermission


SAFE_METHODS = ["GET", "HEAD", "OPTIONS"]


class IsAdminOrReadOnly(BasePermission):
    """
    The user is an authenticated admin, or an endpoint is read-only.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user and request.user.is_staff:
            return True
        return False
