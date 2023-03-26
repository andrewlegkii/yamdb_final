from rest_framework import permissions
from users.models import ADMIN, MODERATOR


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated and user.role == ADMIN
                or user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))


class IsAuthorOrModeratorOrAdminOrReadOnly(
        permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == MODERATOR
