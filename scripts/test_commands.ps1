# Scripts de PowerShell para testing

# Ejecutar todos los tests
function Test-All {
    python test_runner.py all
}

# Ejecutar solo tests unitarios
function Test-Unit {
    python test_runner.py unit
}

# Ejecutar solo tests de integración
function Test-Integration {
    python test_runner.py integration
}

# Ejecutar tests con cobertura
function Test-Coverage {
    python test_runner.py coverage
}

# Ejecutar tests rápidos
function Test-Fast {
    python test_runner.py fast
}

# Ejecutar tests específicos por categoría
function Test-Models {
    python test_runner.py models
}

function Test-Forms {
    python test_runner.py forms
}

function Test-Views {
    python test_runner.py views
}

function Test-Auth {
    python test_runner.py auth
}

# Limpiar archivos de cache de pytest
function Clean-TestCache {
    Remove-Item -Recurse -Force .pytest_cache -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force .coverage -ErrorAction SilentlyContinue
    Write-Host "✅ Cache de testing limpiado"
}

# Instalar dependencias de testing
function Install-TestDeps {
    Write-Host "📦 Instalando dependencias de testing..."
    pip install -r requirements-dev.txt
    Write-Host "✅ Dependencias instaladas"
}

# Función de ayuda
function Test-Help {
    Write-Host @"
🧪 Scripts de Testing para Meet & Gig

Funciones disponibles:
    Test-All          - Ejecutar todos los tests
    Test-Unit         - Solo tests unitarios  
    Test-Integration  - Solo tests de integración
    Test-Models       - Solo tests de modelos
    Test-Forms        - Solo tests de formularios
    Test-Views        - Solo tests de vistas
    Test-Auth         - Solo tests de autenticación
    Test-Coverage     - Tests con reporte de cobertura
    Test-Fast         - Tests rápidos (sin migraciones)
    Clean-TestCache   - Limpiar cache de pytest
    Install-TestDeps  - Instalar dependencias de testing
    Test-Help         - Mostrar esta ayuda

Ejemplos de uso:
    Test-All
    Test-Unit
    Test-Coverage
    Clean-TestCache
"@
}

# Mostrar ayuda por defecto
Test-Help
