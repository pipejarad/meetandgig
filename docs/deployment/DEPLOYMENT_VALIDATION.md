# GUÍA DE DESPLIEGUE SEGURO - Meet & Gig

## Validación de Instalación Desde Cero

Esta guía garantiza que el código funcione correctamente en una instalación limpia.

## 1. CLONAR Y CONFIGURAR

```bash
git clone [repositorio]
cd meetandgig
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows
pip install -r requirements.txt
```

## 2. CONFIGURAR BASE DE DATOS

```bash
# Crear migraciones (si es necesario)
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar estado
python manage.py showmigrations usuarios
```

## 3. POBLAR DATOS INICIALES

```bash
# Crear superusuario
python manage.py createsuperuser

# Cargar datos de prueba (si existen fixtures)
python manage.py loaddata fixtures/*.json
```

## 4. VALIDAR INSTALACIÓN

```bash
# Ejecutar validaciones
python validate_system.py

# Verificar sistema
python manage.py check --deploy
```

## 5. PROBAR FUNCIONALIDAD

```bash
# Iniciar servidor
python manage.py runserver

# Probar URLs principales:
# - http://127.0.0.1:8000/ (inicio)
# - http://127.0.0.1:8000/registro/ (registro)
# - http://127.0.0.1:8000/admin/ (admin)
```

## ARQUITECTURA ACTUAL

### Modelos Principales:

- **Usuario**: Modelo de autenticación base
- **PerfilMusico**: Datos personales del músico
- **Portafolio**: Datos profesionales y portfolio público
- **Instrumento, Genero, NivelExperiencia, Ubicacion**: Catálogos normalizados

### Relaciones M2M:

- **PortafolioInstrumento**: Instrumentos del portafolio con prioridad
- **PortafolioGenero**: Géneros musicales con prioridad
- **Multimedia**: Archivos y enlaces del portafolio
- **Testimonio**: Referencias y testimonios

### Formularios:

- **PerfilMusicoForm**: Datos personales (9 campos)
- **PortafolioForm**: Datos profesionales

## ESTADO DE MIGRACIONES

✅ Las migraciones están en estado CORRECTO  
✅ Base de datos NORMALIZADA correctamente  
✅ Todas las tablas CREADAS y funcionando  
✅ Relaciones M2M RESUELTAS

## VALIDACIÓN DE PRODUCCIÓN

- [x] Modelos funcionan correctamente
- [x] Relaciones M2M accesibles
- [x] Formularios validan correctamente
- [x] Servidor ejecuta sin errores
- [x] Migraciones en estado consistente
- [x] Templates renderizan correctamente

## ¿INSTALACIÓN DESDE CERO FUNCIONARÁ?

**SÍ** - El sistema está completamente validado para instalaciones limpias.

Ejecutar: `python validate_system.py` después de `python manage.py migrate`
