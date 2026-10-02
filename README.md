# Renta Testa - Plataforma E-Commerce Industrial

Renta Testa es una plataforma integral de comercio electrónico diseñada para la gestión operativa de arriendos de maquinaria pesada, venta de materiales de construcción y contratación de servicios especializados. 

Este proyecto fue estructurado bajo arquitecturas escalables, implementando reglas de negocio transaccionales, seguridad basada en control de acceso por roles (RBAC) y la orquestación de servicios a través de una API RESTful.

---

## Arquitectura y Stack Tecnológico

- **Backend:** Python 3, Django, Django REST Framework (DRF).
- **Autenticación:** JSON Web Tokens (JWT) mediante `djangorestframework-simplejwt` con control dinámico de expiración y asimetría de privilegios.
- **Frontend:** Server-Side Rendering (SSR) híbrido con Vanilla JavaScript (ES6+), HTML5 y Tailwind CSS (v3).
- **Base de Datos:** PostgreSQL (Sistema de Gestión de Bases de Datos Relacionales).
- **Seguridad:** Aislamiento de credenciales mediante variables de entorno (`python-dotenv`).
- **Documentación de API:** `drf-spectacular` (OpenAPI 3.0 / Swagger UI).
- **Filtrado Avanzado:** `django-filter` para consultas dinámicas y parametrizadas sobre colecciones de la API.
- **Procesamiento de Archivos:** `Pillow` para la validación, carga y almacenamiento de representaciones multimedia.

---

## Especificaciones Técnicas y Reglas de Negocio

### 1. Transaccionalidad y Consistencia de Inventario (ACID)
El flujo de checkout implementa el decorador `@transaction.atomic` para garantizar la integridad referencial y prevenir condiciones de carrera (Race Conditions) durante escenarios de concurrencia. La confirmación de pago bloquea temporalmente la base de datos para:
1. Validar la disponibilidad de inventario en tiempo real.
2. Aplicar deducción atómica de stock.
3. Instanciar el registro histórico del contrato.
4. Purgar el carrito de compras del usuario.
*Las operaciones de cancelación o devolución ejecutan un rollback semántico, reponiendo el stock de la maquinaria de forma automatizada.*

### 2. Seguridad JWT y Control de Acceso (RBAC)
El control de autorización se maneja mediante políticas estrictas inyectadas en las capas de DRF:
- **Roles y Permisos:** Implementación de clases de permisos customizadas (`IsCliente`, `IsEjecutivo`) que validan la firma y el payload (Claims) del JWT.
- **Expiración Dinámica:** 
  - *Clientes:* Tokens persistentes (24 horas) para optimización del embudo de conversión.
  - *Ejecutivos:* Tokens efímeros (2 minutos). Si la sesión de administración se encuentra inactiva, el token expira para mitigar ataques de secuestro de sesión sobre el inventario.

### 3. Panel de Administración y Manipulación de Recursos (Dashboard)
Subsistema CRUD exclusivo para el rol administrativo. Capacidades operativas:
- Manipulación de entidades (Maquinarias, Materiales, Especialistas).
- Consumo de la API mediante `FormData` para la persistencia de imágenes en formato binario hacia el backend.
- Modificación asíncrona (AJAX/Fetch) minimizando la recarga del DOM.

### 4. Persistencia de Carrito (Relación OneToOne)
El carrito de compras implementa una relación `OneToOneField` vinculada a la instancia de `AbstractUser`. Esto asegura la persistencia del estado en la base de datos transaccional, independientemente de la sesión local del cliente.

---

## Instrucciones de Despliegue Local

### 1. Preparación de la Base de Datos
Requiere instancia activa de PostgreSQL. A través de `psql` o interfaz gráfica (pgAdmin), inicialice el esquema:
```sql
CREATE DATABASE renting_db;
```

### 2. Configuración de Entorno Virtual
```bash
git clone https://github.com/Rodryxb/renta-testa.git
cd renta-testa
python -m venv venv
```
Activación del entorno:
- Entornos Windows: `.\venv\Scripts\activate`
- Entornos UNIX: `source venv/bin/activate`

### 3. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configuración de Variables de Entorno
Duplique `.env.example` hacia `.env` y proceda a inyectar sus credenciales de conexión PostgreSQL y llave criptográfica.

### 5. Migraciones
Sincronice los modelos de la aplicación con la base de datos relacional:
```bash
python manage.py makemigrations renting
python manage.py migrate
```

### 6. Ejecución del Servidor WSGI
```bash
python manage.py runserver
```
Servicio disponible en `http://127.0.0.1:8000/`.

---

## Documentación OpenAPI
El proyecto despliega automáticamente esquemas formales bajo la especificación OpenAPI.
Interfaz interactiva Swagger UI disponible en: **[http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)**
