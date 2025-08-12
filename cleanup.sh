#!/bin/bash
# Limpieza de workspace para conversaciones de Copilot
# Usar: chmod +x cleanup.sh && ./cleanup.sh

echo "🧹 Limpiando archivos temporales revividos..."

# Eliminar archivos no trackeados
git clean -fd

# Verificar estado
git status

echo "✅ Workspace limpio y listo"
