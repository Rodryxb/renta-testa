# Renta Testa - Plataforma E-Commerce Industrial

## Descripción del Proyecto
Renta Testa es una plataforma integral de comercio electrónico diseñada para la gestión operativa de arriendos de maquinaria pesada y la venta de materiales de construcción. Este proyecto fue desarrollado como evaluación práctica integral para la asignatura de Desarrollo Backend y Frontend, demostrando la implementación de arquitecturas escalables, reglas de negocio complejas, transacciones seguras y el consumo de APIs RESTful.

## Tecnologías y Arquitectura
- **Backend:** Python, Django, Django REST Framework.
- **Autenticación:** JSON Web Tokens (JWT) mediante SimpleJWT con expiración dinámica por Roles.
- **Frontend:** HTML5, Vanilla JavaScript (ES6+), Tailwind CSS (v3).
- **Base de Datos:** PostgreSQL (Sistema Relacional Principal).
- **Seguridad:** Variables de entorno (`python-dotenv`) para protección de credenciales y llaves secretas.
- **Documentación de API:** drf-spectacular (OpenAPI / Swagger UI).
- **Procesamiento de Archivos:** Pillow (Para carga estructurada de recursos multimedia).

## Características Principales

- **Procesamiento de Checkout y Gestión de Stock (Transaccionalidad):** 
  Flujo de compras real. Cuando un usuario finaliza el pago, el backend utiliza `@transaction.atomic` de Django para bloquear la base de datos, validar stock, descontar el inventario físico en tiempo real, crear el registro histórico del contrato y vaciar el carrito. Todo esto previene compras simultáneas de ítems agotados (condiciones de carrera).

- **Seguridad Dinámica JWT por Roles (RBAC):** 
  El sistema de inicio de sesión analiza el rol del usuario que solicita acceso:
  - **Ejecutivos (Admins):** Se emite un Token con una expiración estricta de **2 minutos** para proteger la administración del inventario contra abandono de sesión.
  - **Clientes:** Se emite un Token con una duración extendida de **24 horas**, priorizando una experiencia de compra fluida y sin interrupciones.

- **Panel de Administración (Dashboard):** 
  Sistema CRUD protegido para gestionar el inventario de maquinaria, materiales, servicios externos y configuración dinámica de la interfaz web, incluyendo soporte completo para subida de imágenes (FormData).

- **Código Estructurado y Altamente Documentado:** 
  Las reglas de negocio (Modelos) y los controladores (Vistas API) cuentan con exhaustiva documentación y comentarios en el código fuente (explicando relaciones OneToOne, properties matemáticas, transacciones y lógica de roles), pensado para facilitar el análisis académico y escalabilidad futura.

## Instalación y Despliegue Local

1. Clonar el repositorio en el equipo local:
   ```bash
   git clone https://github.com/Rodryxb/renta-testa.git
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   .env\Scriptsctivate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar Variables de Entorno:
   - Copiar el archivo `.env.example` y renombrarlo a `.env`.
   - Modificar las credenciales dentro del archivo `.env` con los datos de tu conexión local a PostgreSQL y definir una `SECRET_KEY`.

5. Aplicar las migraciones a la base de datos:
   ```bash
   python manage.py migrate
   ```

6. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

El proyecto estará disponible en `http://127.0.0.1:8000/`.

---
*Proyecto de carácter académico desarrollado para INACAP.*
