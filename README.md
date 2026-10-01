# Renta Testa - Plataforma E-Commerce Industrial

## Descripción del Proyecto
Renta Testa es una plataforma integral de comercio electrónico diseñada para la gestión operativa de arriendos de maquinaria pesada y la venta de materiales de construcción. Este proyecto fue desarrollado como evaluación práctica integral para la asignatura de Desarrollo Backend y Frontend, demostrando la implementación de arquitecturas escalables, reglas de negocio complejas y el consumo de APIs RESTful.

## Tecnologías y Arquitectura
- **Backend:** Python, Django, Django REST Framework.
- **Autenticación:** JSON Web Tokens (JWT) gestionado a través de SimpleJWT.
- **Frontend:** HTML5, Vanilla JavaScript (ES6+), Tailwind CSS (v3).
- **Base de Datos:** PostgreSQL (Sistema Relacional Principal).
- **Documentación de API:** drf-spectacular (OpenAPI / Swagger UI).
- **Procesamiento de Archivos:** Pillow (Para carga estructurada de recursos multimedia).

## Características Principales
- **Panel de Administración (Dashboard):** Sistema CRUD protegido por roles de usuario para gestionar el inventario de maquinaria, materiales, servicios externos y configuración de la interfaz.
- **Lógica de Cotización Avanzada:** Cálculo dinámico de contratos de arriendo que considera tarifas diarias, factores de uso técnico, restricciones de fechas (máximo 21 días), costos logísticos por zona geográfica (Norte, Central, Sur) y retención de garantías.
- **Carro de Compras Dinámico:** Integración asíncrona que permite gestionar compras de materiales y reservas de maquinaria en una sola sesión, aplicando reglas de negocio automatizadas (ej. descuentos por volumen).
- **Control de Acceso (RBAC):** Separación estricta de privilegios entre perfiles de "Cliente" (cotización y reservas) y "Ejecutivo" (administración total de la plataforma).
- **Interactividad Asíncrona:** Consumo de la API REST mediante Fetch API para actualizaciones de estado, validación de formularios y carga de archivos binarios (FormData) sin recarga de la página.

## Instalación y Despliegue Local

1. Clonar el repositorio en el equipo local:
   ```bash
   git clone https://github.com/Rodryxb/renta-testa.git
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

4. Aplicar las migraciones a la base de datos:
   ```bash
   python manage.py migrate
   ```

5. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

El proyecto estará disponible en `http://127.0.0.1:8000/`.

---
*Proyecto de carácter académico desarrollado para INACAP.*
