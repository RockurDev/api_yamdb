from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows full access to admin users for create, update,
    and delete operations. Non-admin users can only perform read operations.
    """

    def has_permission(self, request: Request, view) -> bool:
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Permission that allows moderators to edit or delete any content.
    Non-moderator users can only perform read operations.
    """

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and (
            request.user == obj.author
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsSuperuserOrAdmin(permissions.BasePermission):
    """
    Permission that grants full access to superusers regardless of their role,
    and to admin users based on their role. Superusers always have full rights.
    """

    def has_permission(self, request: Request, view) -> bool:
        return request.user.is_superuser or (
            request.user.is_authenticated and request.user.is_admin
        )
