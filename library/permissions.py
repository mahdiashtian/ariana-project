from rest_framework import permissions


class RoleBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)

        match role:
            case 'ADMIN':
                return True

            case 'EDITOR':
                match request.method:
                    case 'DELETE':
                        return False
                    case _:
                        return True

            case 'VIEWER':
                if request.method in permissions.SAFE_METHODS:
                    return True
                return False

            case _:
                return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
