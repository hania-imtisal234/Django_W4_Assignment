from rest_framework.permissions import BasePermission


class IsAdminOrReadOnlyForOthers(BasePermission):
    """
    Custom permission class that grants different access levels based on the user's role.

    - Admin users (superusers) have full access to the view.
    - Non-admin users (doctors and patients) have read-only access.

    Permissions:
    - Admin users: Full access (GET, POST, PUT, DELETE, etc.)
    - Non-admin users: Read-only access (GET, HEAD, OPTIONS)

    Methods:
    - `has_permission(self, request, view)`: Checks if the request method is allowed based on the user's role.
    - `has_object_permission(self, request, view, obj)`: Checks if the request method is allowed based on the user's role and the object being accessed.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        return request.method in ['GET', 'HEAD', 'OPTIONS']

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.method in ['GET', 'HEAD', 'OPTIONS']


class IsAdminOnly(BasePermission):
    """
    Custom permission class that grants full access only to admin users (superusers).

    Permissions:
    - Admin users: Full access (GET, POST, PUT, DELETE, etc.)
    - Non-admin users: No access (403 Forbidden)

    Methods:
    - `has_permission(self, request, view)`: Checks if the user is a superuser (admin) to grant full access.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        return False
