# Limpieza de workspace para conversaciones de Copilot
# Usar: .\cleanup.ps1

Write-Host "🧹 Limpiando archivos temporales revividos..." -ForegroundColor Yellow

# Eliminar archivos no trackeados
git clean -fd

# Verificar estado  
git status

Write-Host "✅ Workspace limpio y listo" -ForegroundColor Green
