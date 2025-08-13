# MeetAndGig 🎵

**Plataforma digital para conectar músicos con empleadores para eventos en vivo**

## 📋 Descripción

MeetAndGig es una aplicación web desarrollada en Django que facilita la conexión entre músicos talentosos y empleadores que buscan entretenimiento en vivo para sus eventos. La plataforma permite a los músicos crear perfiles profesionales y a los empleadores encontrar el talento perfecto para sus ocasiones especiales.

## ✨ Características Principales

### 🎯 Sprint 1: Autenticación y Acceso Básico (100% COMPLETADO)

- ✅ **Ticket 1.1**: Registro de usuario con validación de email único y contraseña
- ✅ **Ticket 1.2**: Inicio de sesión con validación de credenciales y persistencia
- ✅ **Ticket 1.3**: Cierre de sesión que destruye sesión y redirige al login
- ✅ **Ticket 1.4**: Recuperación de contraseña con envío de enlace por correo
- ✅ **Ticket 1.5**: Acceso al panel de administración para superusuarios
- ✅ **Ticket 1.6**: Diseño responsivo y amigable para pantallas de login

### 🎼 Sprint 2: Perfiles de Usuario (90% COMPLETADO)

- ✅ **Ticket 2.1**: Crear y editar perfil de músico (administrativo/personal)
- ✅ **Ticket 2.2**: Crear y editar perfil de empleador (organización, contacto)
- ✅ **Ticket 2.3**: Subida de foto de perfil con carga y visualización
- ✅ **Ticket 2.4**: Vista del portafolio del músico (página pública profesional)
- ✅ **Ticket 2.5**: Crear y editar contenido del portafolio (instrumentos, géneros, multimedia)
- 🔄 **Ticket 2.6**: Diseño de pantallas de perfil (incluye ruta /p/<slug>/ y SEO básico)
- ✅ **Ticket 2.7**: Validación de unicidad de perfil (un usuario = un perfil + un portafolio)
- ✅ **Ticket 2.8**: Sistema completo de búsqueda y filtrado de portafolios con catálogos normalizados
- ✅ **Ticket 2.9**: Normalización de categorías con 63 instrumentos, 28 géneros, management commands y admin avanzado

### � Sprint 3: Publicación y Ofertas Laborales (PENDIENTE)

- 🔄 **Ticket 3.1**: Crear oferta laboral (formulario para empleadores)
- 🔄 **Ticket 3.2**: Visualizar ofertas publicadas (listado accesible a músicos)
- 🔄 **Ticket 3.3**: Filtrar ofertas por criterios (estilo, instrumento, ubicación, fecha)
- 🔄 **Ticket 3.4**: Cerrar oferta laboral (cambiar estado a "cerrada")
- 🔄 **Ticket 3.5**: Diseño de vista de ofertas (UI responsive)
- 🔥 **Ticket 3.6**: Postulación a una oferta laboral (desde vista de oferta)
- 🔥 **Ticket 3.7**: Validaciones de postulaciones y cierre (evitar duplicidad, control cupos)

### 🎭 Sprint 4: Visualización, Referencias y Moderación (PENDIENTE)

- 🔄 **Ticket 4.1**: Agregar referencia laboral al portafolio
- 🔄 **Ticket 4.2**: Visualizar referencias laborales en portafolio
- 🔄 **Ticket 4.3**: Mostrar información de contacto según configuración
- 🔄 **Ticket 4.4**: Notificar postulación a empleador (email/alerta)
- � **Ticket 4.5**: Notificar resultado de postulación al músico
- 🔄 **Ticket 4.6**: Revisar y aceptar/rechazar postulaciones
- 🔄 **Ticket 4.7**: Vista de estado de postulación para músicos
- 🔄 **Ticket 4.8**: Funcionalidad de moderación básica (admin)
- 🔄 **Ticket 4.9**: Diseño responsive general (móvil/escritorio)

### 👥 Tipos de Usuario

- **Músicos**: Artistas que buscan oportunidades de presentación
- **Empleadores**: Organizadores de eventos que necesitan entretenimiento

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.9+
- pip (gestor de paquetes de Python)
- Git

### Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/pipejarad/meetandgig.git
cd meetandgig
```

2. **Crear entorno virtual**

```bash
python -m venv venv
```

3. **Activar entorno virtual**

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Aplicar migraciones**

```bash
python manage.py migrate
```

6. **Crear superusuario (opcional)**

```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo**

```bash
python manage.py runserver
```

8. **Acceder a la aplicación**

- Aplicación: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 🧪 Testing

Ejecutar todos los tests:

```bash
python manage.py test
```

Ejecutar tests específicos:

```bash
python manage.py test usuarios
```

Ver cobertura de tests:

```bash
python manage.py test usuarios -v 2
```

## 📁 Estructura del Proyecto

```
meetandgig/
├── docs/                    # 📚 Documentación organizada
│   ├── tickets/            # Tickets completados con detalles técnicos
│   ├── desarrollo/         # Documentación de implementaciones M2M, templates
│   ├── fases/             # Documentación de fases completadas
│   ├── mejoras/           # Mejoras visuales y limpieza del proyecto
│   ├── deployment/        # Validaciones para despliegue
│   ├── guias/             # Guías de templates y contexto del proyecto
│   └── README.md          # Índice de documentación
├── meetandgig/             # ⚙️ Configuración principal
│   ├── settings.py        # Configuraciones de Django
│   ├── urls.py           # URLs principales del proyecto
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes, Bootstrap)
│   └── wsgi.py          # Configuración WSGI para producción
├── usuarios/              # 👥 App de gestión de usuarios y portafolios
│   ├── models.py         # Usuario, PerfilMusico, Portafolio, Genero, Instrumento (+7 modelos)
│   ├── forms.py          # Formularios de registro, login, perfiles y portafolios
│   ├── views.py          # Vistas de autenticación, perfiles y portafolios
│   ├── admin.py          # Admin personalizado con filtros y búsqueda
│   ├── urls.py           # URLs específicas de usuarios
│   ├── backends.py       # Backend de autenticación con email personalizado
│   ├── tests.py          # Suite de tests completa
│   ├── migrations/       # Migraciones de BD (12 migraciones, incluye M2M)
│   └── templates/usuarios/  # Templates HTML específicos
│       ├── login.html           # Página de login
│       ├── registro.html        # Página de registro
│       ├── inicio.html          # Página principal
│       ├── editar_perfil_musico.html      # Formulario perfil (datos personales)
│       ├── ver_perfil_musico.html         # Vista perfil (datos personales)
│       ├── editar_portafolio_musico.html  # Formulario portafolio (datos profesionales)
│       ├── ver_portafolio_musico.html     # Vista portafolio público
│       ├── perfil_empleador.html          # Vista perfil empleador
│       ├── perfil_empleador_form.html     # Formulario empleador
│       ├── crear_perfil_empleador.html    # Creación empleador
│       ├── editar_perfil_empleador.html   # Edición empleador
│       ├── recuperar_password.html        # Recuperación de contraseña
│       └── cambiar_password.html          # Cambio de contraseña
├── templates/             # 🎨 Templates base del proyecto
│   └── base.html         # Template base con Bootstrap 4, navbar dinámico, mensajes
├── media/                # 📁 Archivos subidos por usuarios
│   ├── fotos_perfil/     # Fotos de perfil de usuarios
│   └── portafolios/      # Multimedia de portafolios (imágenes, videos)
├── staticfiles/          # 📦 Archivos estáticos recolectados para producción
├── TICKETS.md            # 📋 Backlog principal con estado de todos los tickets
├── guidelines.md         # 📖 Convenciones y mejores prácticas de desarrollo
├── requirements.txt      # 📦 Dependencias de producción
├── requirements-dev.txt  # 🛠️ Dependencias adicionales para desarrollo
└── manage.py            # 🐍 Comando principal de Django
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.20 (framework web principal)
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción recomendada)
- **Frontend**: Bootstrap 4.3.1, HTML5, CSS3, JavaScript ES6
- **Autenticación**: Sistema personalizado con email como username + tokens seguros
- **Multimedia**: Sistema de subida con ImageField, soporte video/audio embebido
- **Arquitectura**: Separación PerfilMusico (datos personales) / Portafolio (datos profesionales)
- **Relaciones M2M**: Géneros musicales e instrumentos normalizados
- **Templates**: Sistema jerárquico con base.html, bloques reutilizables
- **Formularios**: Django Forms con validación personalizada y contadores
- **Localización**: Configurado para Chile (es-CL, CLP)
- **Testing**: Django TestCase con cobertura completa
- **Control de versiones**: Git con conventional commits
- **Documentación**: Markdown organizado en carpeta docs/

## 📊 Estado del Desarrollo

### ✅ Completado (Sprint 1 y 2)

#### 🎯 Sprint 1: Autenticación Completa (100%)

- [x] **Sistema de autenticación robusto**
  - ✅ Registro con validación de email único
  - ✅ Login con email/username + persistencia de sesión
  - ✅ Logout con redirección segura
  - ✅ Recuperación de contraseña con tokens y emails
  - ✅ Acceso al panel de administración
  - ✅ Templates responsive con diseño profesional

#### 🎼 Sprint 2: Sistema de Perfiles y Portafolios (90%)

- [x] **Arquitectura separada de datos**

  - ✅ PerfilMusico: datos personales/administrativos
  - ✅ Portafolio: datos profesionales públicos
  - ✅ Separación clara de responsabilidades

- [x] **Modelos relacionales avanzados**

  - ✅ 7+ modelos: Usuario, PerfilMusico, Portafolio, Genero, Instrumento, etc.
  - ✅ Relaciones M2M normalizadas para géneros e instrumentos
  - ✅ Campos profesionales: biografía, formación, experiencia, tarifas
  - ✅ Enlaces sociales: YouTube, Spotify, SoundCloud, Instagram, Facebook

- [x] **Sistema completo de formularios**

  - ✅ Formularios de perfil (datos personales)
  - ✅ Formularios de portafolio (datos profesionales)
  - ✅ Formularios de empleador (organizaciones)
  - ✅ Validación personalizada y contadores de caracteres
  - ✅ Subida de fotos de perfil con preview

- [x] **Templates profesionales**

  - ✅ Vista de perfil personal (administrativo)
  - ✅ Vista de portafolio público (profesional)
  - ✅ Diseño consistente y responsive
  - ✅ Integración con Bootstrap 4
  - ✅ Sistema de mensajes automático

- [x] **Sistema de búsqueda y catálogos**
  - ✅ Búsqueda avanzada de portafolios con filtros múltiples
  - ✅ Catálogos normalizados: 63 instrumentos, 28 géneros, ubicaciones
  - ✅ Management commands para poblado automático
  - ✅ Admin interface avanzado con estadísticas de uso
  - ✅ Tests completos de funcionalidad

#### 🏗️ Infraestructura y Calidad

- [x] **Base sólida del proyecto**

  - ✅ Configuración optimizada de Django 4.2.20
  - ✅ Backend de autenticación personalizado
  - ✅ Sistema de manejo de archivos multimedia
  - ✅ 12 migraciones de BD optimizadas y limpias
  - ✅ Suite completa de tests funcionales
  - ✅ Documentación técnica organizada en docs/

- [x] **Limpieza y organización**
  - ✅ Código limpio siguiendo principios DRY
  - ✅ Eliminación de archivos temporales y cache
  - ✅ Restructuración de documentación por temas
  - ✅ Guidelines de desarrollo establecidas

### 🔄 En Desarrollo

#### 🎼 Sprint 2: Funcionalidades Finales (10%)

- [ ] **Ticket 2.6**: Diseño de pantallas de perfil

  - Rutas públicas `/p/<slug>/` para portafolios
  - SEO básico para portafolios (meta tags, structured data)
  - Mejoras visuales y UI/UX finales

### 📋 Planificado

#### � Sprint 3: Ofertas Laborales

- [ ] Sistema completo de ofertas de trabajo
- [ ] Formularios para empleadores
- [ ] Visualización y filtrado de ofertas
- [ ] Sistema de postulaciones
- [ ] Validaciones y control de cupos

#### 🎭 Sprint 4: Referencias y Moderación

- [ ] Sistema de referencias laborales
- [ ] Notificaciones por email
- [ ] Panel de moderación
- [ ] Gestión de postulaciones
- [ ] Estadísticas y reportes

## 🚀 Cómo Empezar

### 📋 Prerrequisitos

- Python 3.9+ (probado con Python 3.9)
- pip (gestor de paquetes de Python)
- Git para control de versiones
- Editor de código (recomendado: VS Code)

### ⚡ Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/meetandgig.git
cd meetandgig

# 2. Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser

# 6. Ejecutar servidor de desarrollo
python manage.py runserver
```

### 🌐 Acceso al Sistema

Una vez iniciado el servidor:

- **🏠 Página principal**: http://127.0.0.1:8000/
- **👤 Registro de usuario**: http://127.0.0.1:8000/usuarios/registro/
- **🔐 Login**: http://127.0.0.1:8000/usuarios/login/
- **⚙️ Admin Panel**: http://127.0.0.1:8000/admin/ (requiere superusuario)

### 🗂️ Datos de Prueba

Para poblar catálogos con datos reales:

```bash
python manage.py poblar_catalogos
```

Esto añadirá:

- **63 instrumentos** organizados en 5 categorías (Cuerdas, Vientos, Percusión, Teclas, Folclore Chileno)
- **28 géneros musicales** con descripciones detalladas
- **16 ubicaciones** principales de Chile
- **4 niveles de experiencia** estructurados

### 🧪 Testing

Ejecutar la suite completa de tests:

```bash
python manage.py test
```

Tests específicos disponibles:

- `test_perfil_form.py` - Validación de formularios
- `test_portafolio_completo.py` - Sistema de portafolios
- `test_m2m_fields.py` - Relaciones many-to-many
- `test_enlaces_sociales.py` - Validación de redes sociales

## 🧑‍💻 Desarrollo

### Convenciones de Código

- Seguir las guías establecidas en `meetandgig/guidelines.md`
- Código limpio y principios DRY
- Tests obligatorios para nuevas funcionalidades
- Mensajes de commit descriptivos

### Workflow de Git

```bash
# Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commit
git add .
git commit -m "feat: descripción de la funcionalidad"

# Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

## 📝 Contribución

1. Fork el repositorio
2. Crear rama de funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## ‍💻 Autor

**Felipe Jara** ([@pipejarad](https://github.com/pipejarad))

---

⭐ **¡Dale una estrella al repo si te gusta el proyecto!**
