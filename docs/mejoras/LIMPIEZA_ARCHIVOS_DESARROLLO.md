# GUÍA DE LIMPIEZA - ARCHIVOS DE DESARROLLO

## 📋 ANÁLISIS DE ARCHIVOS CREADOS DURANTE EL DESARROLLO

### 🗂️ **CATEGORÍAS DE ARCHIVOS**

---

## ✅ **ARCHIVOS SEGUROS PARA ELIMINAR**

### **Scripts de Testing Temporales**

```bash
test_m2m_fields.py                  # ✅ Eliminar - Test específico M2M ya validado
test_perfil_form.py                 # ✅ Eliminar - Test de formulario ya validado
test_template_perfil.py             # ✅ Eliminar - Test de template ya validado
test_template_portafolio.py         # ✅ Eliminar - Test de template ya validado
```

### **Scripts de Verificación de Base de Datos**

```bash
check_all_tables.py                 # ✅ Eliminar - Diagnóstico temporal
check_instrumento_table.py          # ✅ Eliminar - Verificación específica completada
check_tables.py                     # ✅ Eliminar - Diagnóstico temporal
validate_system.py                  # ✅ Eliminar - Validación completada
```

---

## ⚠️ **ARCHIVOS A CONSERVAR TEMPORALMENTE**

### **Scripts de Migración**

```bash
migrate_portafolio_data.py          # ⚠️  CONSERVAR - Podría necesitarse para rollback
populate_catalogs.py                # ⚠️  CONSERVAR - Útil para reconstruir catálogos
```

**Razón**: Si necesitas hacer rollback o recrear datos, estos scripts son valiosos.

---

## 📚 **DOCUMENTACIÓN - EVALUAR SEGÚN NECESIDAD**

### **Documentación de Proceso**

```bash
CAMPOS_M2M_IMPLEMENTADOS.md         # 🤔 OPCIONAL - Excelente para referencia futura
CORRECCION_TEMPLATE_PERFIL.md       # 🤔 OPCIONAL - Historial de correcciones
CORRECCIÓN_TEMPLATE_PERFIL.md       # 🤔 OPCIONAL - Duplicado? Verificar contenido
DEPLOYMENT_VALIDATION.md            # 🤔 OPCIONAL - Útil para deployments futuros
FORMULARIO_PERFIL_CORREGIDO.md      # 🤔 OPCIONAL - Historial de correcciones
MEJORA_TEMPLATE_PORTAFOLIO.md       # 🤔 OPCIONAL - Historial de mejoras
PROBLEMA_RESUELTO_PERFIL_MUSICO.md  # 🤔 OPCIONAL - Historial de problemas
```

### **Documentación de Tickets/Fases**

```bash
FASE_3_COMPLETADA.md                # 📝 CONSERVAR - Historial de proyecto
FASE_3_COMPLETADA_REFACTOR.md       # 📝 CONSERVAR - Historial de refactor
TICKET_*.md                         # 📝 CONSERVAR - Historial de desarrollo
TICKETS.md                          # 📝 CONSERVAR - Índice de tickets
```

---

## 🏠 **ARCHIVOS PERMANENTES DEL PROYECTO**

### **Core del Proyecto**

```bash
manage.py                           # 🏠 PERMANENTE - Core Django
requirements.txt                    # 🏠 PERMANENTE - Dependencias producción
requirements-dev.txt                # 🏠 PERMANENTE - Dependencias desarrollo
db.sqlite3                          # 🏠 PERMANENTE - Base de datos
```

### **Configuración y Documentación Esencial**

```bash
README.md                           # 🏠 PERMANENTE - Documentación principal
guidelines.md                       # 🏠 PERMANENTE - Guías de desarrollo
TEMPLATES_GUIDE.md                  # 🏠 PERMANENTE - Guía de templates
copilot-project-context.md          # 🏠 PERMANENTE - Contexto del proyecto
```

---

## 🎯 **RECOMENDACIÓN DE LIMPIEZA**

### **FASE 1: Limpieza Inmediata (100% Segura)**

```bash
# Eliminar scripts de testing temporales
Remove-Item "test_m2m_fields.py"
Remove-Item "test_perfil_form.py"
Remove-Item "test_template_perfil.py"
Remove-Item "test_template_portafolio.py"

# Eliminar scripts de verificación
Remove-Item "check_all_tables.py"
Remove-Item "check_instrumento_table.py"
Remove-Item "check_tables.py"
Remove-Item "validate_system.py"
```

### **FASE 2: Evaluación de Documentación (Opcional - Después de 1 semana)**

```bash
# Evaluar si necesitas conservar historial detallado
# Si no lo necesitas, puedes eliminar:
# - CORRECCION_TEMPLATE_PERFIL.md (duplicados)
# - Documentos de problemas específicos ya resueltos
```

### **FASE 3: Limpieza de Migración (Después de confirmar que todo funciona - 1 mes)**

```bash
# Una vez confirmado que no necesitas rollback:
# Remove-Item "migrate_portafolio_data.py"
#
# Si los catálogos están estables:
# Remove-Item "populate_catalogs.py"
```

---

## 💡 **CRITERIOS DE DECISIÓN**

### **¿Cuándo eliminar un archivo?**

- ✅ **Scripts de test**: Si el feature funciona correctamente ➜ **ELIMINAR**
- ✅ **Scripts de diagnóstico**: Si el problema está resuelto ➜ **ELIMINAR**
- ⚠️ **Scripts de migración**: Si podrías necesitar rollback ➜ **CONSERVAR**
- 📝 **Documentación**: Si proporciona valor histórico/referencia ➜ **CONSERVAR**
- 🗑️ **Documentación**: Si es redundante o muy específica ➜ **ELIMINAR**

### **¿Qué conservar siempre?**

- 🏠 Archivos core del proyecto Django
- 📝 Documentación de tickets/fases (historial)
- 🔧 Configuración y guías generales
- ⚠️ Scripts de migración (hasta confirmar estabilidad)

---

## 🎉 **RESULTADO ESPERADO DESPUÉS DE LIMPIEZA**

### **Estructura Limpia:**

```
meetandgig/
├── 🏠 manage.py
├── 🏠 requirements.txt
├── 🏠 requirements-dev.txt
├── 🏠 db.sqlite3
├── 📝 README.md
├── 📝 guidelines.md
├── 📝 TEMPLATES_GUIDE.md
├── 📝 TICKETS.md
├── 📝 TICKET_*.md
├── 📝 FASE_*.md
├── ⚠️ migrate_portafolio_data.py (temporal)
├── ⚠️ populate_catalogs.py (temporal)
├── 🤔 CAMPOS_M2M_IMPLEMENTADOS.md (referencia)
└── 🏠 [directorios del proyecto...]
```

**Beneficios:**

- ✅ Proyecto más limpio y organizado
- ✅ Sin archivos obsoletos que confundan
- ✅ Conserva historial importante
- ✅ Mantiene capacidad de rollback temporal
