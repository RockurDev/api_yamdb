from typing import Any
from rest_framework import permissions
from rest_framework.request import Request


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows full access to admin users for create, update,
    and delete operations. Non-admin users can only perform read operations.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_admin


class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Permission that allows moderators to edit or delete any content.
    Non-moderator users can only perform read operations.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_moderator


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission that allows users to edit or delete only their own content.
    Non-owners can only perform read operations.
    """

    def has_object_permission(
        self, request: Request, view: Any, obj: Any
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow edit and delete only if the object belongs to the current user
        return obj.author == request.user


class IsSuperuserOrAdmin(permissions.BasePermission):
    """
    Permission that grants full access to superusers regardless of their role,
    and to admin users based on their role. Superusers always have full rights.
    """

    def has_permission(self, request: Request, view: Any) -> bool:
        # Superusers always have full access
        if request.user.is_superuser:
            return True

        # Admins have full access
        return request.user.is_authenticated and request.user.is_admin
