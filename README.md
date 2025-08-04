# MeetAndGig 🎵

**Plataforma digital para conectar músicos con empleadores para eventos en vivo**

## 📋 Descripción

MeetAndGig es una aplicación web desarrollada en Django que facilita la conexión entre músicos talentosos y empleadores que buscan entretenimiento en vivo para sus eventos. La plataforma permite a los músicos crear perfiles profesionales y a los empleadores encontrar el talento perfecto para sus ocasiones especiales.

## ✨ Características Principales

### 🎯 Sprint 1: Autenticación y Acceso Básico

- ✅ **Ticket 1.1**: Sistema de registro completo con validación de email único
- ✅ **Ticket 1.2**: Sistema de login con autenticación por email/username
- ✅ **Ticket 1.3**: Sistema de logout con botón en header
- ✅ **Ticket 1.4**: Sistema de recuperación de contraseña con tokens seguros
- 📋 **Ticket 1.5**: Acceso a panel de administración
- 📋 **Ticket 1.6**: Diseño mejorado de login/registro
- 📋 **Ticket 1.7**: Upgrade Bootstrap 4 → Bootstrap 5

### 🎼 Sprint 2: Gestión de Perfiles de Músico

- ✅ **Ticket 2.1**: Sistema completo de perfiles de músico con portafolio profesional
- 📋 **Ticket 2.10**: Vista pública del portafolio del músico

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
├── meetandgig/           # Configuración principal
│   ├── settings.py       # Configuraciones de Django
│   ├── urls.py          # URLs principales
│   ├── static/          # Archivos estáticos (CSS, JS, imágenes)
│   └── guidelines.md    # Guías de desarrollo
├── usuarios/            # App de gestión de usuarios
│   ├── models.py        # Usuario, PerfilMusico con 20+ campos
│   ├── forms.py         # Formularios de registro, login y perfiles
│   ├── views.py         # Vistas de autenticación y perfiles
│   ├── urls.py          # URLs específicas de usuarios
│   ├── admin.py         # Configuración del admin de Django
│   ├── backends.py      # Backend de autenticación personalizado
│   ├── tests.py         # Suite de tests (11 tests)
│   ├── migrations/      # Migraciones de base de datos
│   └── templates/       # Templates HTML específicos
│       └── usuarios/
│           ├── editar_perfil_musico.html
│           └── ver_perfil_musico.html
├── templates/           # Templates base del proyecto
│   └── base.html        # Template base con Bootstrap 4
├── media/              # Archivos subidos por usuarios
│   ├── fotos_perfil/   # Fotos de perfil de usuarios
│   └── portafolios/    # Multimedia de portafolios
├── TICKETS.md          # Documentación de todos los tickets
├── TEMPLATES_GUIDE.md  # Guía de templates
├── requirements.txt    # Dependencias de producción
├── requirements-dev.txt # Dependencias de desarrollo
└── manage.py          # Comando de Django
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.20
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: Bootstrap 4.3.1, HTML5, CSS3, JavaScript
- **Autenticación**: Sistema personalizado con email como username
- **Multimedia**: Sistema de subida de archivos con ImageField
- **Validación**: Formularios Django con validación personalizada
- **Localización**: Configuración para Chile (es-cl, CLP)
- **Testing**: Django TestCase
- **Control de versiones**: Git

## 📊 Estado del Desarrollo

### ✅ Completado

#### 🎯 Sprint 1: Autenticación Completa

- [x] **Ticket 1.1**: Sistema de registro completo con validación de email único
- [x] **Ticket 1.2**: Sistema de login con autenticación por email/username
- [x] **Ticket 1.3**: Sistema de logout con botón en header
- [x] **Ticket 1.4**: Sistema de recuperación de contraseña con tokens seguros

#### 🎼 Sprint 2: Perfiles de Músico

- [x] **Ticket 2.1**: Sistema completo de perfiles de músico
  - ✅ Modelo PerfilMusico con 20+ campos profesionales
  - ✅ Formularios de creación y edición con validación
  - ✅ Sistema de subida de fotos de perfil
  - ✅ Campos para instrumentos, géneros y experiencia
  - ✅ Enlaces a redes sociales y multimedia
  - ✅ Tarifas en pesos chilenos (CLP)
  - ✅ Configuración de privacidad y disponibilidad
  - ✅ Templates responsive con Bootstrap 4
  - ✅ Validación de formularios y contadores de caracteres

#### 🏗️ Infraestructura

- [x] Configuración inicial del proyecto Django 4.2.20
- [x] Modelo de usuario personalizado con tipos (músico/empleador)
- [x] Backend de autenticación personalizado con email
- [x] Sistema de manejo de archivos multimedia
- [x] Configuración de URLs y settings optimizada
- [x] Templates base responsivos con Bootstrap 4.3.1
- [x] Suite completa de tests (11/11 pasando)
- [x] Migraciones de base de datos optimizadas

### 🔄 En Desarrollo

#### 🎯 Sprint 1: Finalización

- [ ] **Ticket 1.5**: Acceso a panel de administración
- [ ] **Ticket 1.6**: Diseño mejorado de login/registro
- [ ] **Ticket 1.7**: Upgrade Bootstrap 4 → Bootstrap 5

#### 🎼 Sprint 2: Portafolios Públicos

- [ ] **Ticket 2.10**: Vista pública del portafolio del músico

### 📋 Planificado

#### 🎯 Sprint 2: Gestión Completa de Perfiles

- [ ] **Ticket 2.2**: Dashboard personalizado para músicos
- [ ] **Ticket 2.3**: Sistema de búsqueda de músicos
- [ ] **Ticket 2.4**: Filtros avanzados por instrumento/género/ubicación
- [ ] **Ticket 2.5**: Perfiles de empleadores
- [ ] **Ticket 2.6**: Normalización de categorías
- [ ] **Ticket 2.7**: Sistema de favoritos
- [ ] **Ticket 2.8**: Estadísticas de perfil
- [ ] **Ticket 2.9**: Configuración de notificaciones

#### 🎯 Sprint 3: Funcionalidades Avanzadas

- [ ] Sistema de mensajería interna
- [ ] Sistema de calificaciones y reseñas
- [ ] Gestión de eventos y contrataciones
- [ ] Integración de pagos
- [ ] Calendario de disponibilidad
- [ ] Sistema de notificaciones push

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
