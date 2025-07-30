# Template System - Meet & Gig

## Estructura de Templates

La estructura de templates ha sido organizada de manera jerárquica para facilitar la extensión y mantenimiento:

```
meetandgig/
├── templates/
│   ├── index.html          # Template base principal
│   └── base.html           # Template base con navegación
└── usuarios/
    └── templates/
        └── usuarios/
            ├── base.html   # Template base para usuarios
            ├── login.html  # Página de login
            ├── registro.html # Página de registro
            └── inicio.html # Página de inicio
```

## Jerarquía de Templates

1. **index.html** - Template raíz con toda la estructura HTML, CSS y JS
2. **base.html** - Extiende index.html y añade navegación global
3. **usuarios/base.html** - Extiende base.html para la app de usuarios
4. **Páginas específicas** - Extienden usuarios/base.html

## Cómo usar los Templates

### Para crear una nueva página en usuarios:

```django
{% extends 'usuarios/base.html' %}

{% block title %}Mi Nueva Página - Meet & Gig{% endblock %}

{% block usuarios_content %}
<div class="row">
    <div class="col-12">
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
{% endblock %}
```

### Para crear una nueva aplicación:

1. Crea tu aplicación: `python manage.py startapp mi_app`
2. Crea la estructura de templates:
   ```
   mi_app/
   └── templates/
       └── mi_app/
           ├── base.html
           └── pagina.html
   ```
3. En `mi_app/templates/mi_app/base.html`:

   ```django
   {% extends "base.html" %}

   {% block main_content %}
       {% block mi_app_content %}
       <!-- Contenido específico de mi_app -->
       {% endblock %}
   {% endblock %}
   ```

## Bloques Disponibles

### En index.html (template raíz):

- `{% block title %}` - Título de la página
- `{% block meta_description %}` - Meta descripción
- `{% block extra_css %}` - CSS adicional
- `{% block navbar %}` - Barra de navegación
- `{% block sidebar %}` - Menú lateral
- `{% block messages %}` - Mensajes de Django
- `{% block content %}` - Contenido principal
- `{% block extra_js %}` - JavaScript adicional

### En base.html (con navegación):

- `{% block main_content %}` - Contenido principal dentro del contenedor

### En usuarios/base.html:

- `{% block usuarios_content %}` - Contenido específico de usuarios

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

La navegación se configura en `templates/base.html`. Para agregar elementos:

```django
<li class="nav-item">
    <a class="nav-link" href="{% url 'mi_vista' %}">Mi Página</a>
</li>
```

## Mensajes de Django

Los mensajes se muestran automáticamente en todas las páginas:

```python
# En tus views
from django.contrib import messages

messages.success(request, 'Operación exitosa')
messages.error(request, 'Error en la operación')
messages.warning(request, 'Advertencia')
messages.info(request, 'Información')
```

## Consejos de Desarrollo

1. **Siempre usa `{% load static %}`** al inicio de tus templates
2. **Usa URLs con nombres** en lugar de rutas hardcodeadas: `{% url 'nombre_url' %}`
3. **Mantén la consistencia** usando los bloques apropiados
4. **Aprovecha los componentes Bootstrap** incluidos
5. **Personaliza con CSS** en lugar de modificar los archivos base

## Próximos Pasos

1. Crear más aplicaciones siguiendo esta estructura
2. Añadir un sistema de permisos y roles
3. Implementar AJAX para formularios dinámicos
4. Añadir un sidebar con navegación secundaria
5. Implementar temas personalizables
