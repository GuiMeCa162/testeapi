from rest_framework import permissions

class IsAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.tipo == "admin":
            return True
        return False
    
class IsStaffPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.tipo in ["admin", "staff"]:
            return True
        return False
    
class IsAdminOrOwnerStaffPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if IsAdminPermission().has_permission(request, view):
            return True
        elif IsStaffPermission().has_permission(request, view) and obj == user:
            return True
        return False