from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model has an 'owner' or 'user' field.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.owner == request.user if hasattr(obj, 'owner') else obj.user == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    Read-only access for everyone else.
    """
    
    def has_permission(self, request, view):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for admins
        return request.user and request.user.is_staff


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user if hasattr(obj, 'owner') else obj.user == request.user


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Allow unauthenticated users to create (POST) but require authentication for other methods.
    Useful for registration endpoints.
    """
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class IsVerifiedUser(permissions.BasePermission):
    """
    Permission to only allow verified users.
    Assumes the user model has an 'is_email_verified' field.
    """
    
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'is_email_verified', True)
        )


class IsSuperUser(permissions.BasePermission):
    """
    Permission to only allow superusers.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class HasAPIKey(permissions.BasePermission):
    """
    Permission to check for valid API key in headers.
    """
    
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        # Implement your API key validation logic here
        # For example, check against a database of valid API keys
        return api_key is not None  # Simplified example


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to allow owners or admins to access an object.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admins have full access
        if request.user and request.user.is_staff:
            return True
        
        # Owners have access to their own objects
        return obj.owner == request.user if hasattr(obj, 'owner') else obj.user == request.user


class ReadOnly(permissions.BasePermission):
    """
    Permission to only allow read-only access.
    """
    
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
