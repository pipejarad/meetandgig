# MeetAndGig 🎵

**Plataforma digital para conectar músicos con empleadores para eventos en vivo**

[![Django](https://img.shields.io/badge/Django-4.2.20-green.svg)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-4.3.1-purple.svg)](https://getbootstrap.com)
[![Tests](https://img.shields.io/badge/Tests-34/34_passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)]()

## 📋 Descripción

MeetAndGig es una aplicación web desarrollada en Django que facilita la conexión entre músicos talentosos y empleadores que buscan entretenimiento en vivo para sus eventos. La plataforma permite a los músicos crear perfiles profesionales y a los empleadores encontrar el talento perfecto para sus ocasiones especiales.

## ✨ Características Principales

### 🎯 Sprint 1: Autenticación y Acceso Básico (✅ 100% COMPLETADO)

- ✅ **Ticket 1.1**: Registro de usuario con validación de email único y contraseña
- ✅ **Ticket 1.2**: Inicio de sesión con validación de credenciales y persistencia
- ✅ **Ticket 1.3**: Cierre de sesión que destruye sesión y redirige al login
- ✅ **Ticket 1.4**: Recuperación de contraseña con envío de enlace por correo
- ✅ **Ticket 1.5**: Acceso al panel de administración para superusuarios
- ✅ **Ticket 1.6**: Diseño responsivo y amigable para pantallas de login

### 🎼 Sprint 2: Perfiles de Usuario (✅ 100% COMPLETADO)

- ✅ **Ticket 2.1**: Crear y editar perfil de músico (administrativo/personal)
- ✅ **Ticket 2.2**: Crear y editar perfil de empleador (organización, contacto)
- ✅ **Ticket 2.3**: Subida de foto de perfil con carga y visualización
- ✅ **Ticket 2.4**: Vista del portafolio del músico (página pública profesional)
- ✅ **Ticket 2.5**: Crear y editar contenido del portafolio (instrumentos, géneros, multimedia)
- ✅ **Ticket 2.6**: Diseño de pantallas de perfil (incluye ruta /p/<slug>/ y SEO básico)
- ✅ **Ticket 2.7**: Validación de unicidad de perfil (un usuario = un perfil + un portafolio)
- ✅ **Ticket 2.8**: Sistema completo de búsqueda y filtrado de portafolios con catálogos normalizados
- ✅ **Ticket 2.9**: Normalización de categorías con 63 instrumentos, 28 géneros, management commands y admin avanzado

### 🎸 Sprint 3: Ofertas Laborales y Postulaciones (✅ 100% COMPLETADO)

- ✅ **Ticket 3.1**: Sistema completo de creación de ofertas laborales
- ✅ **Ticket 3.2**: Visualización pública de ofertas con diseño responsive
- ✅ **Ticket 3.3**: Filtros avanzados por instrumentos, géneros, ubicación, presupuesto y fechas
- ✅ **Ticket 3.4**: Gestión de estado de ofertas (cerrar/reabrir con validaciones)
- ✅ **Ticket 3.5**: UI mobile-first con offcanvas, acordeones y sincronización
- ✅ **Ticket 3.6**: Sistema de postulaciones con validaciones, sidebar dinámico y estados visuales
- ✅ **Ticket 3.7**: Validaciones completas, gestión de postulaciones y notificaciones automáticas
- ✅ **Ticket 3.8**: Sistema de invitaciones directas con dashboard y notificaciones

### 🎭 Sprint 4: Referencias y Moderación (🔄 PLANIFICADO)

- 🔄 **Ticket 4.1**: Agregar referencia laboral al portafolio
- 🔄 **Ticket 4.2**: Visualizar referencias laborales en portafolio
- 🔄 **Ticket 4.3**: Mostrar información de contacto según configuración
- 🔄 **Ticket 4.4**: Notificar postulación a empleador (email/alerta)
- 🔄 **Ticket 4.5**: Notificar resultado de postulación al músico
- 🔄 **Ticket 4.6**: Revisar y aceptar/rechazar postulaciones
- 🔄 **Ticket 4.7**: Vista de estado de postulación para músicos
- 🔄 **Ticket 4.8**: Funcionalidad de moderación básica (admin)
- 🔄 **Ticket 4.9**: Diseño responsive general (móvil/escritorio)

### 👥 Tipos de Usuario

- **Músicos**: Artistas que buscan oportunidades de presentación

  - Crear perfil profesional con portafolio público
  - Buscar y postularse a ofertas laborales
  - Recibir y gestionar invitaciones directas
  - Gestionar referencias y testimonios

- **Empleadores**: Organizadores de eventos que necesitan entretenimiento
  - Publicar ofertas laborales detalladas
  - Buscar músicos por filtros específicos
  - Gestionar postulaciones recibidas
  - Enviar invitaciones directas a músicos

## 🚀 Funcionalidades Implementadas

### 🔐 Sistema de Autenticación

- Registro con email único y validación segura
- Login con email/username + persistencia de sesión
- Recuperación de contraseña con tokens seguros
- Backend personalizado para autenticación con email

### 👤 Gestión de Perfiles

- **Músicos**: Datos personales + Portafolio profesional público
- **Empleadores**: Información organizacional completa
- Subida de fotos de perfil con optimización
- Separación clara entre datos privados y públicos

### 🎵 Sistema de Portafolios

- Páginas públicas profesionales con SEO básico
- Biografía, formación musical y experiencia
- Enlaces a redes sociales (YouTube, Spotify, SoundCloud, etc.)
- Sistema de multimedia para fotos y videos
- Configuración de visibilidad por secciones

### 🎸 Ofertas Laborales

- Creación completa de ofertas con formularios avanzados
- Visualización pública responsive con paginación
- Sistema de filtros múltiples (instrumentos, géneros, ubicación, presupuesto)
- Gestión de estados (borrador, publicada, cerrada, cancelada)
- Control de cupos y fechas límite

### 📝 Sistema de Postulaciones

- Postulación con mensaje personalizado y tarifa propuesta
- Validaciones de duplicidad y control de cupos
- Estados de postulación (pendiente, en revisión, aceptada, rechazada)
- Sistema de cancelación por parte del músico

### 💌 Invitaciones Directas

- Empleadores pueden invitar músicos específicos
- Sistema de aceptación/rechazo con mensajes
- Control de expiración automática
- Conversión automática a postulaciones al aceptar

### 🔔 Sistema de Notificaciones

- Notificaciones automáticas para empleadores
- Estados de lectura/no lectura
- Eventos: postulaciones, invitaciones, ofertas completadas

### 🔍 Búsqueda Avanzada

- **Portafolios**: Por instrumentos, géneros, ubicación, experiencia
- **Ofertas**: Por múltiples criterios con ordenamiento
- Filtros dinámicos con actualización en tiempo real
- Integración con catálogos normalizados

### 📊 Catálogos Normalizados

- **63 instrumentos** en 5 categorías organizadas
- **28 géneros musicales** con descripciones
- **Ubicaciones** de Chile con regiones
- **Niveles de experiencia** estructurados
- Management commands para poblar datos

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
- **Testing**: Django TestCase con 34 tests y 100% de cobertura
- **Control de versiones**: Git con conventional commits
- **Documentación**: Markdown organizado en carpeta docs/

## 🚀 Instalación y Configuración

### 📋 Requisitos Previos

- Python 3.9+ (probado con Python 3.9)
- pip (gestor de paquetes de Python)
- Git para control de versiones
- Editor de código (recomendado: VS Code)

### ⚡ Instalación Rápida

```bash
# 1. Clonar el repositorio
git clone https://github.com/pipejarad/meetandgig.git
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

# 5. Poblar catálogos con datos reales
python manage.py poblar_catalogos

# 6. Crear superusuario (opcional)
python manage.py createsuperuser

# 7. Ejecutar servidor de desarrollo
python manage.py runserver
```

### 🌐 Acceso al Sistema

Una vez iniciado el servidor:

- **🏠 Página principal**: http://127.0.0.1:8000/
- **👤 Registro de usuario**: http://127.0.0.1:8000/usuarios/registro/
- **🔐 Login**: http://127.0.0.1:8000/usuarios/login/
- **🎵 Buscar músicos**: http://127.0.0.1:8000/buscar/
- **💼 Ver ofertas**: http://127.0.0.1:8000/ofertas/
- **⚙️ Admin Panel**: http://127.0.0.1:8000/admin/ (requiere superusuario)

### 🗂️ Datos de Prueba

El comando `poblar_catalogos` añade:

- **63 instrumentos** organizados en 5 categorías (Cuerdas, Vientos, Percusión, Teclas, Folclore Chileno)
- **28 géneros musicales** con descripciones detalladas
- **16 ubicaciones** principales de Chile
- **4 niveles de experiencia** estructurados

## 🧪 Testing

### ✅ Suite Completa de Tests (34/34 pasando)

```bash
# Ejecutar todos los tests
python manage.py test

# Tests específicos por funcionalidad
python manage.py test usuarios.tests_ofertas_laborales    # 15 tests
python manage.py test usuarios.tests_postulaciones       # 8 tests
python manage.py test usuarios.tests_invitaciones        # 8 tests
python manage.py test usuarios.tests_notificaciones      # 3 tests

# Ver detalles de ejecución
python manage.py test -v 2
```

### 📊 Cobertura de Tests

| **Funcionalidad**        | **Tests** | **Cobertura** | **Estado**   |
| ------------------------ | --------- | ------------- | ------------ |
| **Ofertas Laborales**    | 15/15     | 100%          | ✅ Completo  |
| **Postulaciones**        | 8/8       | 100%          | ✅ Completo  |
| **Invitaciones**         | 8/8       | 100%          | ✅ Completo  |
| **Notificaciones**       | 3/3       | 100%          | ✅ Completo  |
| **Perfiles/Portafolios** | -         | Legacy        | ✅ Funcional |

### 🎯 Tests Incluyen

- **Modelos**: Validación de campos, métodos, relaciones
- **Vistas**: Autenticación, permisos, respuestas HTTP
- **Formularios**: Validación de datos y reglas de negocio
- **Búsquedas**: Filtros, parámetros, resultados esperados
- **Flujos Completos**: Desde creación hasta finalización

## 📁 Estructura del Proyecto

```
meetandgig/
├── docs/                    # 📚 Documentación organizada
│   ├── tickets/            # Tickets completados con detalles técnicos
│   ├── sprints/            # Documentación de sprints completados
│   ├── guides/             # Guías de desarrollo y contexto
│   └── PROJECT_STATUS.md   # Estado actual del proyecto
├── meetandgig/             # ⚙️ Configuración principal
│   ├── settings.py        # Configuraciones de Django
│   ├── urls.py           # URLs principales del proyecto
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes, Bootstrap)
│   └── wsgi.py          # Configuración WSGI para producción
├── usuarios/              # 👥 App principal (usuarios, perfiles, ofertas)
│   ├── models.py         # 16 modelos: Usuario, Portafolio, OfertaLaboral, etc.
│   ├── forms.py          # Formularios de registro, perfiles, ofertas
│   ├── views.py          # Vistas de autenticación, perfiles, ofertas (1600+ líneas)
│   ├── admin.py          # Admin personalizado con filtros y búsqueda
│   ├── urls.py           # 25+ URLs específicas de la aplicación
│   ├── backends.py       # Backend de autenticación personalizado
│   ├── tests_*.py        # 4 archivos de tests (34 tests total)
│   ├── migrations/       # 21 migraciones de BD optimizadas
│   ├── management/       # Commands personalizados (poblar_catalogos)
│   └── templates/usuarios/  # 30+ templates HTML específicos
│       ├── auth/              # Templates de autenticación
│       ├── perfiles/          # Templates de perfiles y portafolios
│       ├── ofertas/           # Templates de ofertas laborales
│       └── dashboard/         # Templates de dashboards
├── templates/             # 🎨 Templates base del proyecto
│   └── base.html         # Template base con Bootstrap 4, navbar dinámico
├── media/                # 📁 Archivos subidos por usuarios
│   ├── fotos_perfil/     # Fotos de perfil de usuarios
│   └── portafolios/      # Multimedia de portafolios
├── staticfiles/          # 📦 Archivos estáticos recolectados
├── TICKETS.md            # 📋 Backlog con estado de tickets
├── guidelines.md         # 📖 Convenciones de desarrollo
├── requirements.txt      # 📦 Dependencias de producción
└── manage.py            # 🐍 Comando principal de Django
```

### 🏗️ Arquitectura de Modelos

```
Usuario (AbstractUser)
├── PerfilMusico (datos personales/administrativos)
├── PerfilEmpleador (datos organizacionales)
└── Portafolio (datos profesionales públicos)
    ├── PortafolioInstrumento (M2M con metadata)
    ├── PortafolioGenero (M2M con prioridades)
    ├── Multimedia (imágenes/videos/audio)
    └── Testimonio (referencias)

OfertaLaboral
├── OfertaInstrumento (instrumentos requeridos)
├── OfertaGenero (géneros preferidos)
├── Postulacion (músicos aplicando)
├── Invitacion (invitaciones directas)
└── Notificacion (alertas para empleadores)

Catálogos Normalizados:
├── Instrumento (63 items en 5 categorías)
├── Genero (28 géneros musicales)
├── NivelExperiencia (4 niveles estructurados)
└── Ubicacion (16 ubicaciones de Chile)
```

## 📊 Estado del Desarrollo

### ✅ Completado (Sprints 1-3) - 100%

#### 🎯 Sprint 1: Autenticación Completa

- [x] **Sistema de autenticación robusto**
  - ✅ Registro con validación de email único
  - ✅ Login con email/username + persistencia de sesión
  - ✅ Logout con redirección segura
  - ✅ Recuperación de contraseña con tokens y emails
  - ✅ Acceso al panel de administración
  - ✅ Templates responsive con diseño profesional

#### 🎼 Sprint 2: Sistema de Perfiles y Portafolios

- [x] **Arquitectura separada de datos**

  - ✅ PerfilMusico: datos personales/administrativos
  - ✅ Portafolio: datos profesionales públicos
  - ✅ PerfilEmpleador: datos organizacionales

- [x] **Modelos relacionales avanzados**

  - ✅ 16 modelos interconectados
  - ✅ Relaciones M2M normalizadas para géneros e instrumentos
  - ✅ Campos profesionales: biografía, formación, experiencia, tarifas
  - ✅ Enlaces sociales: YouTube, Spotify, SoundCloud, Instagram, Facebook

- [x] **Sistema completo de formularios y templates**

  - ✅ 30+ templates responsive con Bootstrap 4
  - ✅ Formularios con validación y contadores de caracteres
  - ✅ Sistema de búsqueda avanzada con filtros múltiples
  - ✅ Subida de archivos multimedia optimizada

- [x] **Catálogos normalizados**
  - ✅ 63 instrumentos, 28 géneros, 16 ubicaciones, 4 niveles
  - ✅ Management commands para poblado automático
  - ✅ Admin interface avanzado con estadísticas

#### � Sprint 3: Ofertas Laborales y Postulaciones

- [x] **Sistema completo de ofertas**

  - ✅ Creación, edición y gestión de ofertas laborales
  - ✅ Filtros avanzados (instrumentos, géneros, ubicación, presupuesto, fechas)
  - ✅ Sistema de estados (borrador, publicada, cerrada, cancelada)
  - ✅ Control de cupos y fechas límite

- [x] **Sistema de postulaciones**

  - ✅ Postulación con validaciones de duplicidad
  - ✅ Estados de postulación y control de flujo
  - ✅ Mensajes personalizados y tarifas propuestas
  - ✅ Sistema de cancelación

- [x] **Invitaciones directas**

  - ✅ Empleadores pueden invitar músicos específicos
  - ✅ Sistema de aceptación/rechazo con expiración
  - ✅ Conversión automática a postulaciones

- [x] **Sistema de notificaciones**
  - ✅ Notificaciones automáticas para empleadores
  - ✅ Estados de lectura y gestión de alertas
  - ✅ Integración con eventos del sistema

### 🧪 Infraestructura y Calidad

- [x] **Testing completo: 34/34 tests pasando (100%)**

  - ✅ Tests de modelos, vistas, formularios y búsquedas
  - ✅ Cobertura completa de Sprint 3
  - ✅ Validación de flujos end-to-end

- [x] **Base sólida del proyecto**
  - ✅ Django 4.2.20 optimizado
  - ✅ 21 migraciones optimizadas
  - ✅ Backend de autenticación personalizado
  - ✅ Documentación técnica organizada

### 🔄 Planificado

#### 🎭 Sprint 4: Referencias, Moderación y Finalización

- [ ] Sistema de referencias laborales
- [ ] Notificaciones por email
- [ ] Panel de moderación avanzado
- [ ] Gestión completa de postulaciones (aceptar/rechazar)
- [ ] Estadísticas y reportes
- [ ] Optimización para producción

## 🧑‍💻 Desarrollo

### 🛠️ Convenciones de Código

Seguir las guías establecidas en `guidelines.md`:

- **Principios DRY** y código limpio autoexplicativo
- **Tests obligatorios** para nuevas funcionalidades
- **Actualizaciones quirúrgicas** mínimamente invasivas
- **Nombres significativos** que revelen intención
- **Retornos tempranos** para mejor legibilidad
- **Manejo de errores** con excepciones apropiadas

### 🔄 Workflow de Git

```bash
# Crear rama para nueva funcionalidad
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commit con conventional commits
git add .
git commit -m "feat: descripción de la funcionalidad"

# Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

### � Métricas Actuales

- **Líneas de código**: ~2000+ líneas (models.py: 1200+, views.py: 1600+)
- **Tests**: 34 tests con 100% de éxito
- **Modelos**: 16 modelos interconectados
- **Templates**: 30+ templates responsive
- **URLs**: 25+ endpoints funcionales
- **Migraciones**: 21 migraciones optimizadas

## 🚀 Próximos Pasos

### 🎯 Sprint 4: Referencias y Moderación

**Tickets prioritarios:**

1. **4.6**: Revisar y aceptar/rechazar postulaciones
2. **4.4**: Notificar postulación a empleador (email)
3. **4.7**: Vista de estado de postulación para músicos
4. **4.1-4.2**: Sistema de referencias laborales
5. **4.8**: Funcionalidad de moderación básica

**Estimación:** 2-3 semanas de desarrollo

### 🌐 Preparación para Producción

- [ ] Configuración de PostgreSQL
- [ ] Variables de entorno para secretos
- [ ] Configuración de servidor web (Nginx/Apache)
- [ ] Sistema de backups automatizados
- [ ] Monitoreo y logging
- [ ] Optimización de performance

## �📝 Contribución

1. **Fork** el repositorio
2. **Crear rama** de funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. **Seguir guidelines** de código establecidas
4. **Agregar tests** para nueva funcionalidad
5. **Commit** cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
6. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
7. **Crear Pull Request** con descripción detallada

### 🏆 Contribuidores

Los contribuidores que agreguen funcionalidades significativas serán reconocidos aquí.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Felipe Jara** ([@pipejarad](https://github.com/pipejarad))

- 🌐 LinkedIn: [Felipe Jara](https://linkedin.com/in/pipejarad)
- 📧 Email: contacto@felipejara.dev

## 🙏 Agradecimientos

- **Django Community** por el excelente framework
- **Bootstrap Team** por el sistema de diseño
- **VS Code** por las herramientas de desarrollo
- **GitHub Copilot** por la asistencia en desarrollo

---

### 📊 Estado del Proyecto

**🎯 MVP Progress: 75% completado**

| Sprint   | Estado         | Progreso | Tests     |
| -------- | -------------- | -------- | --------- |
| Sprint 1 | ✅ Completado  | 100%     | ✅ Legacy |
| Sprint 2 | ✅ Completado  | 100%     | ✅ Legacy |
| Sprint 3 | ✅ Completado  | 100%     | ✅ 34/34  |
| Sprint 4 | 🔄 Planificado | 0%       | 📋 TBD    |

**⭐ ¡Dale una estrella al repo si te gusta el proyecto!**

**🔔 Watch el repositorio para recibir actualizaciones**
