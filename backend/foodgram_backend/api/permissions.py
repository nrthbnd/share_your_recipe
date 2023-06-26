from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Права доступа автору или только чтение."""
        return ((request.method in SAFE_METHODS)
                or (request.user.is_authenticated
                and (obj.author == request.user
                     or request.user.is_admin)))
