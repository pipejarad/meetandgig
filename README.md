# MeetAndGig 🎵

**Plataforma digital para conectar músicos con empleadores para eventos en vivo**

## 📋 Descripción

MeetAndGig es una aplicación web desarrollada en Django que facilita la conexión entre músicos talentosos y empleadores que buscan entretenimiento en vivo para sus eventos. La plataforma permite a los músicos crear perfiles profesionales y a los empleadores encontrar el talento perfecto para sus ocasiones especiales.

## ✨ Características Principales

### 🎯 Sprint 1: Autenticación y Acceso Básico
- ✅ **Ticket 1.1**: Sistema de registro completo con validación de email único
- 🔄 **Ticket 1.2**: Sistema de login con autenticación por email/username
- 📋 **Próximos tickets**: Gestión de perfiles por tipo de usuario

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
│   ├── static/          # Archivos estáticos
│   └── guidelines.md    # Guías de desarrollo
├── usuarios/            # App de gestión de usuarios
│   ├── models.py        # Modelos de Usuario, PerfilMusico, PerfilEmpleador
│   ├── forms.py         # Formularios de registro y login
│   ├── views.py         # Vistas de autenticación
│   ├── backends.py      # Backend de autenticación personalizado
│   ├── tests.py         # Suite de tests (11 tests)
│   └── templates/       # Templates HTML
├── templates/           # Templates base
├── requirements.txt     # Dependencias de producción
├── requirements-dev.txt # Dependencias de desarrollo
└── manage.py           # Comando de Django
```

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 4.2.20
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Autenticación**: Sistema personalizado con email como username
- **Testing**: Django TestCase
- **Control de versiones**: Git

## 📊 Estado del Desarrollo

### ✅ Completado
- [x] Configuración inicial del proyecto
- [x] Modelo de usuario personalizado con tipos (músico/empleador)
- [x] Sistema de registro con validaciones robustas
- [x] Backend de autenticación personalizado
- [x] Templates responsivos con Bootstrap
- [x] Suite completa de tests (11/11 pasando)

### 🔄 En Desarrollo
- [ ] Sistema de login mejorado
- [ ] Gestión de perfiles de usuario
- [ ] Dashboard personalizado por tipo de usuario

### 📋 Planificado
- [ ] Sistema de búsqueda y filtrado
- [ ] Mensajería interna
- [ ] Sistema de calificaciones
- [ ] Integración de pagos

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
