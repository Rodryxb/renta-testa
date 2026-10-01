from rest_framework import permissions

# -------------------------------------------------------------------
# PERMISOS DOCUMENTADOS (Aplicación de RBAC)
# -------------------------------------------------------------------

class IsCliente(permissions.BasePermission):
    '''
    Permiso exclusivo para usuarios autenticados con rol CLIENTE
    (Empresa Constructora).
    '''
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'CLIENTE')

class IsEjecutivo(permissions.BasePermission):
    '''
    Permiso exclusivo para usuarios autenticados con rol EJECUTIVO
    (Administrador de Arriendos).
    '''
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'EJECUTIVO')
