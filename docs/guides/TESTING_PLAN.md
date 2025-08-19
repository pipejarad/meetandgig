# 🧪 Plan de Testing con Pytest - Meet & Gig

## 📋 Índice

1. [Estructura del Proyecto de Testing](#estructura)
2. [Configuración](#configuración)
3. [Tipos de Tests](#tipos-de-tests)
4. [Fixtures y Factories](#fixtures-y-factories)
5. [Ejecución de Tests](#ejecución-de-tests)
6. [Cobertura de Código](#cobertura)
7. [Mejores Prácticas](#mejores-prácticas)
8. [Comandos Útiles](#comandos-útiles)

## 📁 Estructura {#estructura}

```
meetandgig/
├── pytest.ini                 # Configuración de pytest
├── conftest.py                # Fixtures globales
├── test_runner.py             # Script personalizado para ejecutar tests
├── test_commands.ps1          # Scripts de PowerShell para Windows
├── requirements-dev.txt       # Dependencias de desarrollo y testing
├── tests/
│   ├── __init__.py
│   ├── factories/
│   │   └── __init__.py        # Factory Boy factories para crear datos de prueba
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py     # Tests unitarios de modelos
│   │   └── test_forms.py      # Tests unitarios de formularios
│   └── integration/
│       ├── __init__.py
│       ├── test_authentication_views.py    # Tests de flujos de autenticación
│       └── test_profile_views.py          # Tests de flujos de perfiles
└── usuarios/
    ├── tests.py              # Tests existentes (mantener como referencia)
    ├── tests_*.py            # Tests específicos existentes
    └── ...
```

## ⚙️ Configuración {#configuración}

### Dependencias Instaladas

```bash
pip install -r requirements-dev.txt
```

**Librerías principales:**

- `pytest==7.4.4` - Framework de testing
- `pytest-django==4.7.0` - Integración Django-pytest
- `pytest-cov==4.1.0` - Cobertura de código
- `pytest-mock==3.12.0` - Mocking
- `pytest-xdist==3.5.0` - Ejecución paralela
- `factory-boy==3.3.0` - Creación de datos de prueba
- `faker==20.1.0` - Datos fake realistas

### Configuración de pytest (pytest.ini)

```ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = meetandgig.settings
python_files = tests.py test_*.py *_tests.py
addopts = --verbose --tb=short --strict-markers --disable-warnings --reuse-db --nomigrations
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests that might take a while
    authentication: Authentication related tests
    models: Model tests
    views: View tests
    forms: Form tests
```

## 🎯 Tipos de Tests {#tipos-de-tests}

### 1. **Tests Unitarios** (`@pytest.mark.unit`)

- **Modelos**: Validaciones, métodos, propiedades
- **Formularios**: Validaciones, campos requeridos, limpieza de datos
- **Utilidades**: Funciones helper, validadores
- **Aislados**: No dependen de BD externa ni servicios

### 2. **Tests de Integración** (`@pytest.mark.integration`)

- **Vistas**: Flujos completos de usuario
- **Autenticación**: Login, registro, logout
- **Permisos**: Acceso a vistas según tipo de usuario
- **Navegación**: Flujos entre múltiples vistas

### 3. **Tests por Categoría**

- `@pytest.mark.models` - Tests de modelos
- `@pytest.mark.forms` - Tests de formularios
- `@pytest.mark.views` - Tests de vistas
- `@pytest.mark.authentication` - Tests de autenticación

## 🏭 Fixtures y Factories {#fixtures-y-factories}

### Fixtures Principales (conftest.py)

```python
@pytest.fixture
def usuario_musico():
    """Usuario tipo músico para testing"""

@pytest.fixture
def usuario_empleador():
    """Usuario tipo empleador para testing"""

@pytest.fixture
def authenticated_client_musico(client, usuario_musico):
    """Cliente autenticado como músico"""
```

### Factory Boy Factories

```python
# Creación de datos realistas
usuario = UsuarioFactory(tipo_usuario='musico')
perfil = PerfilMusicoFactory(usuario=usuario)
portafolio = PortafolioFactory(usuario=usuario)

# Creación en lote
musicos = UsuarioFactory.create_batch(5, tipo_usuario='musico')
```

## 🚀 Ejecución de Tests {#ejecución-de-tests}

### Método 1: Script Personalizado (Recomendado)

```powershell
# PowerShell (Windows)
. .\test_commands.ps1

Test-All           # Todos los tests
Test-Unit          # Solo unitarios
Test-Integration   # Solo integración
Test-Coverage      # Con cobertura
Test-Fast          # Tests rápidos
```

```bash
# Python directo
python test_runner.py all
python test_runner.py unit
python test_runner.py integration
python test_runner.py coverage
```

### Método 2: Pytest Directo

```bash
# Todos los tests
pytest

# Por categoría
pytest -m unit
pytest -m integration
pytest -m models
pytest -m forms

# Archivo específico
pytest tests/unit/test_models.py

# Test específico
pytest tests/unit/test_models.py::TestUsuarioModel::test_crear_usuario_valido

# Con cobertura
pytest --cov=usuarios --cov-report=html
```

### Método 3: Django Management

```bash
# Mantener compatibilidad con tests existentes
python manage.py test usuarios
```

## 📊 Cobertura de Código {#cobertura}

### Generación de Reportes

```bash
# Reporte en terminal + HTML
pytest --cov=usuarios --cov=meetandgig --cov-report=html --cov-report=term-missing

# Solo HTML
python test_runner.py coverage
```

### Interpretación de Resultados

- **90%+**: Excelente cobertura
- **80-89%**: Buena cobertura
- **70-79%**: Cobertura aceptable
- **<70%**: Necesita mejora

### Archivos Generados

- `htmlcov/index.html` - Reporte visual detallado
- `.coverage` - Datos de cobertura
- Terminal - Resumen inmediato

## 📋 Mejores Prácticas {#mejores-prácticas}

### 1. **Estructura de Tests**

```python
@pytest.mark.unit
@pytest.mark.models
class TestUsuarioModel:
    """Tests unitarios para el modelo Usuario"""

    @pytest.mark.django_db
    def test_crear_usuario_valido(self):
        """Test crear usuario con datos válidos"""
        # Arrange
        usuario_data = {...}

        # Act
        usuario = UsuarioFactory(**usuario_data)

        # Assert
        assert usuario.email == usuario_data['email']
        assert usuario.is_active is True
```

### 2. **Nomenclatura**

- Clases: `TestNombreModelo`, `TestNombreVista`
- Métodos: `test_descripcion_clara_del_comportamiento`
- Archivos: `test_categoria.py`

### 3. **Markers**

```python
@pytest.mark.django_db  # Para tests que usan BD
@pytest.mark.slow       # Para tests que toman tiempo
@pytest.mark.unit       # Para tests unitarios
@pytest.mark.integration  # Para tests de integración
```

### 4. **Datos de Prueba**

```python
# ✅ Usar factories
usuario = UsuarioFactory(email='test@example.com')

# ❌ Evitar datos hardcodeados repetitivos
usuario = Usuario.objects.create(...)
```

### 5. **Assertions Claras**

```python
# ✅ Assertions específicas
assert usuario.email == 'test@example.com'
assert response.status_code == 200
assert 'éxito' in str(messages[0])

# ❌ Assertions vagas
assert usuario
assert response
```

## 🛠️ Comandos Útiles {#comandos-útiles}

### Ejecución

```bash
# Tests específicos por pattern
pytest -k "test_usuario"
pytest -k "not slow"

# Verbose con detalles
pytest -vv --tb=long

# Parar en primer fallo
pytest -x

# Ejecución paralela
pytest -n auto

# Re-ejecutar solo tests fallidos
pytest --lf
```

### Debugging

```bash
# Con debugger
pytest --pdb

# Sin captura de salida
pytest -s

# Solo mostrar errores
pytest -q
```

### Mantenimiento

```bash
# Limpiar cache
rm -rf .pytest_cache htmlcov .coverage

# Verificar sintaxis de tests
pytest --collect-only

# Lista de markers
pytest --markers
```

## 🎯 Plan de Implementación

### Fase 1: Configuración Base ✅

- [x] Instalar dependencias
- [x] Configurar pytest.ini
- [x] Crear fixtures globales
- [x] Crear factories básicas

### Fase 2: Tests Unitarios

- [x] Tests de modelos básicos
- [x] Tests de formularios básicos
- [ ] Tests de validadores personalizados
- [ ] Tests de métodos helper

### Fase 3: Tests de Integración

- [x] Tests de autenticación
- [x] Tests de perfiles
- [ ] Tests de portafolios completos
- [ ] Tests de ofertas laborales

### Fase 4: Optimización

- [ ] Cobertura 90%+
- [ ] Performance testing
- [ ] Tests de seguridad
- [ ] CI/CD integration

## 🚨 Problemas Comunes y Soluciones

### 1. **Import Errors**

```bash
# Error: Import "pytest" could not be resolved
# Solución: Instalar dependencias
pip install -r requirements-dev.txt
```

### 2. **Django DB Issues**

```python
# Error: Database access not allowed
# Solución: Agregar marker
@pytest.mark.django_db
def test_my_function():
    ...
```

### 3. **Factory Boy Errors**

```python
# Error: RelatedObjectDoesNotExist
# Solución: Crear dependencias con SubFactory
class PerfilMusicoFactory(django.DjangoModelFactory):
    usuario = factory.SubFactory(MusicoFactory)
```

### 4. **Slow Tests**

```bash
# Optimizar con:
pytest --reuse-db --nomigrations
```

---

## 🎉 ¡Listo para Testing!

Con esta configuración tienes un sistema de testing profesional que incluye:

- ✅ **Tests unitarios** aislados y rápidos
- ✅ **Tests de integración** completos
- ✅ **Cobertura de código** detallada
- ✅ **Datos de prueba** realistas con Factory Boy
- ✅ **Scripts automatizados** para diferentes escenarios
- ✅ **Documentación completa** de uso

**Próximos pasos:**

1. Instalar dependencias: `pip install -r requirements-dev.txt`
2. Ejecutar tests: `python test_runner.py all`
3. Ver cobertura: `python test_runner.py coverage`
4. Implementar tests específicos según necesidades del proyecto
