import os

PROJECT_DIR = r"C:\Users\rodri\.gemini\antigravity\scratch\renting_project"

fixes = {
    # settings.py
    "BASE_DIR": "BASE_DIR",
    "ALLOWED_HOSTS": "ALLOWED_HOSTS",
    "INSTALLED_APPS": "INSTALLED_APPS",
    "MIDDLEWARE": "MIDDLEWARE",
    "AUTH_USER_MODEL": "AUTH_USER_MODEL",
    "TEMPLATES": "TEMPLATES",
    "BACKEND": "BACKEND",
    "DATABASES": "DATABASES",
    "PASSWORD": "PASSWORD",
    "VALIDATORS": "VALIDATORS",
    "LANGUAGE_CODE": "LANGUAGE_CODE",
    "STATIC_URL": "STATIC_URL",
    "MEDIA_URL": "MEDIA_URL",
    "MEDIA_ROOT": "MEDIA_ROOT",
    "SPECTACULAR_SETTINGS": "SPECTACULAR_SETTINGS",
    "REST_FRAMEWORK": "REST_FRAMEWORK",
    
    # HTML and Views
    "MAQUINARIA": "MAQUINARIA",
    "MATERIAL": "MATERIAL",
    "BAJA": "BAJA",
    "MEDIA": "MEDIA",
    "ALTA": "ALTA",
    "OTRAS": "OTRAS",
    "Arriendo": "Arriendo",
    "API": "API",
    "SpectacularAPIView": "SpectacularAPIView",
    "PÚBLICO": "PÚBLICO",
    "INACAP": "INACAP",
    "Máquinas": "Máquinas",
    "Máquinas": "Máquinas",
    "Catálogo": "Catálogo",
    "access_token": "access_token",
    "auth": "auth",
    "ADMIN": "ADMIN",
    "Authorization": "Authorization",
    "authorization": "Authorization",
    "Ahora": "Ahora",
    "Aquí": "Aquí",
    "Abrir": "Abrir",
    "Accion": "Accion",
    "Acciones": "Acciones",
    "Activas": "Activas",
    "Activo": "Activo",
    "Articulo": "Articulo",
    "Añadir": "Añadir",
    "Aplicar": "Aplicar",
    "Aprobado": "Aprobado",
    "AGREGAR": "AGREGAR",
    "Actualizar": "Actualizar",
    "Aceptar": "Aceptar",
    "Administrador": "Administrador",
    "Admin": "Admin",
    "Ayuda": "Ayuda",
    "Acceso": "Acceso",
    "Autenticación": "Autenticación",
    "Artículos": "Artículos",
    "Antes": "Antes",
    "Otras": "Otras", # Wait, OTRAS is OTRAS
    "Cargar": "Cargar",
    "Guía": "Guía",
    "GUÍA": "GUÍA",
    "TABLA": "TABLA",
    "Autor": "Autor",
    "arr": "arr", # variables
    "Maq": "Maq",
    "Mat": "Mat",
    "api": "api",
    "app": "app",
    "apps": "apps",
    "add": "add",
    "all": "all",
    "auto": "auto",
    "available": "available",
    "await": "await",
    "activate": "activate",
    "active": "active",
    "async": "async",
    "arrays": "arrays",
    "area": "area",
    "args": "args",
    "arg": "arg",
    "auth_view": "auth_view",
    "address": "address",
    "actual": "actual",
    "amount": "amount",
    "append": "append",
    "apply": "apply",
    "attribute": "attribute",
    "avatar": "avatar",
    "Ma": "Ma", # Be careful with short ones
}

def repair_file(filepath):
    abs_path = os.path.join(PROJECT_DIR, filepath)
    if not os.path.exists(abs_path): return
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for bad, good in fixes.items():
        content = content.replace(bad, good)
        
    # Manual surgical fixes
    content = content.replace("class Usuario", "class Usuario")
    content = content.replace("class Maquinaria", "class Maquinaria")
    content = content.replace("class MaquinariaViewSet", "class MaquinariaViewSet")
    content = content.replace("class Material", "class Material")
    content = content.replace("MaquinariaSerializer", "MaquinariaSerializer")
    content = content.replace("Maquinaria.objects", "Maquinaria.objects")
    content = content.replace("Maquinarias", "Maquinarias")
    content = content.replace("Maquinaria", "Maquinaria")
    content = content.replace("Materiales", "Materiales")
    content = content.replace("Material", "Material")
    content = content.replace("authentication", "Authentication")
    content = content.replace("authenticated", "Authenticated")
    content = content.replace("authenticate", "Authenticate")
    content = content.replace("IsEjecutivo(permissions.BasePermission)", "IsEjecutivo(permissions.BasePermission)")
    content = content.replace("IsCliente(permissions.BasePermission)", "IsCliente(permissions.BasePermission)")
    content = content.replace("BasePermission", "BasePermission")
    content = content.replace("ABSTRACT_USER", "ABSTRACT_USER")
    content = content.replace("ABSTRACT_USER", "ABSTRACT_USER")
    content = content.replace("app_name", "app_name")
    content = content.replace("appConfig", "AppConfig")
    content = content.replace("apps", "apps")
    content = content.replace("app", "app")
    content = content.replace("auto_now", "auto_now")
    content = content.replace("auto_now_add", "auto_now_add")
    content = content.replace("auto_now_add", "auto_now_add")
    content = content.replace("max_length", "max_length")
    content = content.replace("blank", "blank")
    content = content.replace("null=True, blank=True", "null=True, blank=True")
    content = content.replace("caz", "caz")
    content = content.replace("cas", "cas")
    content = content.replace("False", "False")
    content = content.replace("False", "False")
    content = content.replace("False", "False")
    content = content.replace("allowóNY", "AllowAny")
    content = content.replace("allowAny", "AllowAny")
    content = content.replace("api", "api")
    content = content.replace("AUTH", "AUTH")
    content = content.replace("auth", "auth")
    content = content.replace("array", "Array")
    content = content.replace("arr", "arr")
    content = content.replace("area", "area")
    content = content.replace("action", "action")
    content = content.replace("actions", "actions")
    content = content.replace("activate", "activate")
    content = content.replace("active", "active")
    content = content.replace("async", "async")
    content = content.replace("await", "await")
    content = content.replace("append", "append")
    content = content.replace("apply", "apply")
    content = content.replace("attribute", "attribute")
    content = content.replace("avatar", "avatar")
    content = content.replace("amount", "amount")
    content = content.replace("address", "address")
    content = content.replace("actual", "actual")
    content = content.replace("add", "add")
    content = content.replace("all", "all")
    content = content.replace("auto", "auto")
    content = content.replace("available", "available")
    content = content.replace("TABLA", "TABLA")
    content = content.replace("GUÍA", "GUÍA")
    content = content.replace("Autor", "Autor")

    # Fix models.py fields
    content = content.replace("models.CharField", "models.CharField")
    content = content.replace("models.Textarea", "models.TextField")
    content = content.replace("models.TextField", "models.TextField")
    content = content.replace("models.DateField", "models.DateField")
    content = content.replace("models.DateTimeField", "models.DateTimeField")
    content = content.replace("models.ImageField", "models.ImageField")
    content = content.replace("models.CASCADE", "models.CASCADE")
    content = content.replace("models.CASCADE", "models.CASCADE")
    
    if original != content:
        with open(abs_path, 'w', encoding='utf-8') as f:
            f.write(content)

for root, dirs, files in os.walk(PROJECT_DIR):
    if 'venv' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.html') or file.endswith('.md'):
            repair_file(os.path.join(root, file))

print("Reparación masiva completada.")
