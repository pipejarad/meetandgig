# Template System - Meet & Gig

## Estructura de Templates

La estructura de templates ha sido organizada de manera jerárquica para facilitar la extensión y mantenimiento:

```
meetandgig/
├── templates/
│   └── base.html           # Template base principal con navegación completa
└── usuarios/
    └── templates/
        └── usuarios/
            ├── login.html           # Página de login
            ├── registro.html        # Página de registro
            ├── inicio.html          # Página de inicio
            ├── recuperar_password.html   # Recuperación de contraseña
            └── cambiar_password.html     # Cambio de contraseña
```

## Jerarquía de Templates

1. **base.html** - Template raíz con toda la estructura HTML, CSS, JS y navegación
2. **Páginas específicas** - Extienden directamente base.html

## Cómo usar los Templates

### Para crear una nueva página en usuarios:

```django
{% extends 'base.html' %}

{% block title %}Mi Nueva Página - Meet & Gig{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4 class="card-title">Mi Nueva Página</h4>
                </div>
                <div class="card-body">
                    <!-- Tu contenido aquí -->
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Para crear una nueva aplicación:

1. Crea tu aplicación: `python manage.py startapp mi_app`
2. Crea la estructura de templates:
   ```
   mi_app/
   └── templates/
       └── mi_app/
           └── mi_pagina.html
   ```
3. En `mi_app/templates/mi_app/mi_pagina.html`:

   ```django
   {% extends "base.html" %}

   {% block title %}Mi App - Meet & Gig{% endblock %}

   {% block content %}
   <div class="container-fluid py-4">
       <!-- Contenido específico de mi_app -->
   </div>
   {% endblock %}
   ```

## Bloques Disponibles

### En base.html (template principal):

- `{% block title %}` - Título de la página
- `{% block meta_description %}` - Meta descripción para SEO
- `{% block extra_css %}` - CSS adicional específico de la página
- `{% block sidebar %}` - Contenido del sidebar/menú lateral
- `{% block messages %}` - Área para mensajes de Django (ya implementada automáticamente)
- `{% block content %}` - Contenido principal de la página
- `{% block extra_js %}` - JavaScript adicional específico de la página

### Estructura del navbar:

El navbar está **integrado** en base.html y **no es un bloque**, sino que está hardcodeado con la lógica de autenticación. Incluye:

- Logo y navegación principal
- Enlaces dinámicos según el estado de autenticación
- Dropdown de usuario para usuarios logueados

### Ejemplo de uso de todos los bloques:

```django
{% extends 'base.html' %}

{% block title %}Login - Meet & Gig{% endblock %}

{% block meta_description %}Inicia sesión en Meet & Gig para conectar músicos con eventos{% endblock %}

{% block extra_css %}
<style>
    .login-form {
        max-width: 400px;
        margin: 0 auto;
    }
</style>
{% endblock %}

{% block sidebar %}
<div class="sidebar-custom">
    <!-- Contenido personalizado del sidebar -->
</div>
{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <!-- Tu contenido principal aquí -->
</div>
{% endblock %}

{% block extra_js %}
<script>
    // JavaScript específico para esta página
</script>
{% endblock %}
```

## Archivos Estáticos

Los archivos estáticos están organizados en:

```
meetandgig/static/
├── css/
│   ├── bootstrap.min.css
│   ├── main.css
│   ├── animate.css
│   ├── flag-icon.min.css
│   └── meetandgig-custom.css  # CSS personalizado
├── js/
│   ├── jquery.min.js
│   ├── bootstrap.bundle.min.js
│   ├── main.js
│   └── ...
├── img/
├── fonts/
└── vendor/
```

### Para usar archivos estáticos:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/mi-estilo.css' %}">
<script src="{% static 'js/mi-script.js' %}"></script>
<img src="{% static 'img/mi-imagen.jpg' %}" alt="Imagen">
```

## Componentes Bootstrap Disponibles

El template incluye Bootstrap 4 y componentes personalizados:

### Cards:

```html
<div class="card">
  <div class="card-header">
    <h4 class="card-title">Título</h4>
  </div>
  <div class="card-body">Contenido</div>
</div>
```

### Formularios:

```html
<div class="mb-3">
  <label for="campo" class="form-label">Etiqueta</label>
  <input type="text" class="form-control" id="campo" />
</div>
```

### Tablas:

```html
<div class="table-responsive">
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Columna</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Datos</td>
      </tr>
    </tbody>
  </table>
</div>
```

## Personalización CSS

Usa `meetandgig-custom.css` para personalizar estilos:

```css
:root {
  --meetandgig-primary: #007bff;
  --meetandgig-secondary: #6c757d;
  /* más variables... */
}

.mi-clase-personalizada {
  /* tus estilos */
}
```

## Navegación

### Navbar Integrado

La navegación está **integrada y fixed** en `templates/base.html` e incluye:

- **Header**: Logo Meet & Gig con enlace al inicio
- **Navegación principal**: Enlaces a las secciones principales
- **Menús dinámicos**: Enlaces que cambian según el estado de autenticación:
  - **Usuario no logueado**: Login y Registro
  - **Usuario logueado**: Dropdown con perfil y logout
- **Mensajes**: Sistema automático de notificaciones Django

⚠️ **Importante**: El navbar **NO es un bloque personalizable**. Está hardcodeado con la lógica de autenticación integrada.

### Para personalizar la navegación:

Si necesitas modificar la navegación, edita directamente el archivo `templates/base.html` en la sección del navbar (líneas ~42-85).

### Ejemplo de estructura actual del navbar:

```django
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'inicio' %}">Meet & Gig</a>

        <!-- Navegación principal -->
        <ul class="navbar-nav me-auto">
            <li class="nav-item">
                <a class="nav-link" href="{% url 'inicio' %}">Inicio</a>
            </li>
        </ul>

        <!-- Navegación de usuario -->
        <ul class="navbar-nav">
            {% if user.is_authenticated %}
                <!-- Dropdown para usuario logueado -->
            {% else %}
                <!-- Enlaces de login/registro -->
            {% endif %}
        </ul>
    </div>
</nav>
```

## Mensajes de Django

### Sistema Automático Integrado

Los mensajes se muestran **automáticamente** en todas las páginas a través del bloque `{% block messages %}` en `base.html`. **No necesitas hacer nada adicional** en tus templates.

### Tipos de mensajes disponibles:

```python
# En tus views
from django.contrib import messages

# Mensaje de éxito (verde)
messages.success(request, 'Operación completada exitosamente')

# Mensaje de error (rojo)
messages.error(request, 'Ocurrió un error en la operación')

# Mensaje de advertencia (amarillo)
messages.warning(request, 'Advertencia: Revisa los datos')

# Mensaje informativo (azul)
messages.info(request, 'Información importante para el usuario')
```

### Personalización de mensajes:

Si necesitas personalizar el **estilo** o **comportamiento** de los mensajes, puedes:

1. **Sobrescribir el bloque messages** en tu template:

```django
{% block messages %}
<div class="custom-messages">
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} custom-alert">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
</div>
{% endblock %}
```

2. **Usar JavaScript personalizado** en `{% block extra_js %}` para efectos especiales.

## Sistema de Sidebar

### Bloque Sidebar Disponible

El template base incluye un bloque `{% block sidebar %}` que puedes usar para añadir contenido lateral específico a ciertas páginas.

### Ejemplo de uso del sidebar:

```django
{% extends 'base.html' %}

{% block title %}Dashboard - Meet & Gig{% endblock %}

{% block sidebar %}
<div class="sidebar-nav">
    <h5>Navegación</h5>
    <ul class="nav flex-column">
        <li class="nav-item">
            <a class="nav-link" href="#perfil">Mi Perfil</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#configuracion">Configuración</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="#historial">Historial</a>
        </li>
    </ul>
</div>
{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <!-- Contenido principal -->
</div>
{% endblock %}
```

**Nota**: La mayoría de páginas actuales **no usan sidebar**, pero está disponible para implementaciones futuras como dashboards de usuario o paneles administrativos.

## Consejos de Desarrollo

1. **Siempre usa `{% load static %}`** al inicio de tus templates si necesitas archivos estáticos
2. **Usa URLs con nombres** en lugar de rutas hardcodeadas: `{% url 'nombre_url' %}`
3. **Extiende directamente base.html** para todas las páginas
4. **Usa el contenedor apropiado**: `<div class="container-fluid py-4">` para páginas completas
5. **Aprovecha los componentes Bootstrap** incluidos
6. **Personaliza con CSS** en el bloque `{% block extra_css %}`
7. **Mantén la consistencia** en el uso de cards y componentes

## Estructura de Página Recomendada

```django
{% extends 'base.html' %}

{% block title %}Título - Meet & Gig{% endblock %}

{% block content %}
<div class="container-fluid py-4">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <div class="card">
                <div class="card-header">
                    <h4 class="card-title">Título de la Sección</h4>
                </div>
                <div class="card-body">
                    <!-- Contenido principal -->
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Próximos Pasos

1. Crear más aplicaciones siguiendo esta estructura
2. Añadir un sistema de permisos y roles
3. Implementar AJAX para formularios dinámicos
4. Añadir un sidebar con navegación secundaria
5. Implementar temas personalizables
