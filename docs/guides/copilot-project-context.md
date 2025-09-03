# Meet & Gig — Contexto del Proyecto

> **Propósito de este archivo**: Dar _contexto funcional, técnico y de producto_

# Meet & Gig — Contexto del Proyecto

> **Propósito de este archivo**: Dar _contexto funcional, técnico y de producto_

\*\*E---

### Notas finales para Copilot

- **MVP COMPLETADO**: Todos los sprints principales (1-4) han sido implementados exitosamente
- **Infraestructura sólida**: Sistema de testing, scripts organizados, documentación completa
- **Estado actual**: Proyecto listo para producción con todas las funcionalidades core implementadas
- **Próximos objetivos**: Optimización, nuevas funcionalidades opcionales, mejoras de UX
- **Referencia oficial**: Usar siempre `TICKETS.md` como fuente de verdad para estados y descripciones
- Revisa `guidelines.md` para estilo, seguridad y PF antes de sugerir cambios.ctual - MVP COMPLETADO (Septiembre 2025):\*\*

- ✅ **Sistema de Autenticación** (Sprint 1)
- ✅ **Perfiles y Portafolios** (Sprint 2)
- ✅ **Ofertas Laborales Completo** (Sprint 3)
- ✅ **Sistema de Referencias Completo** (Sprint 4)
- ✅ **Infraestructura y Testing** (Sprint 5)

**Funcionalidades Implementadas:**

- ✅ Sistema de usuarios autenticados y diferenciados
- ✅ Portafolios profesionales como vitrina pública
- ✅ Sistema completo de ofertas laborales con postulaciones
- ✅ Sistema de referencias laborales con emails seguros
- ✅ Catálogos normalizados para filtros inteligentes
- ✅ Búsqueda avanzada en todas las secciones
- ✅ Notificaciones por email automatizadas
- ✅ Panel de gestión para empleadores
- ✅ Arquitectura escalable y mantenible

---

### Notas finales para Copilot

- **Sprints 1-2 COMPLETADOS**: La arquitectura de perfiles y portafolios está implementada y funcionando
- **Base sólida establecida**: Sistema de autenticación, portafolios públicos, búsqueda, catálogos poblados
- **Próximo objetivo**: Sprint 3 - Sistema de ofertas laborales usando la infraestructura existente
- **Referencia oficial**: Usar siempre `TICKETS.md` como fuente de verdad para estados y descripciones
- Revisa `guidelines.md` para estilo, seguridad y PF antes de sugerir cambios.rimientos del MVP y las convenciones de este repositorio.

---

### Notas finales para Copilot

- **Sprints 1-2 COMPLETADOS**: La arquitectura de perfiles y portafolios está implementada y funcionando
- **Base sólida establecida**: Sistema de autenticación, portafolios públicos, búsqueda, catálogos poblados
- **Próximo objetivo**: Sprint 3 - Sistema de ofertas laborales usando la infraestructura existente
- **Referencia oficial**: Usar siempre `TICKETS.md` como fuente de verdad para estados y descripciones
- Revisa `guidelines.md` para estilo, seguridad y PF antes de sugerir cambios.nition of Done) para Sprint 3

**Próximos objetivos - Sistema de Ofertas Laborales:**

- [ ] Modelo OfertaLaboral con campos requeridos
- [ ] CRUD completo para empleadores (crear, editar, cerrar ofertas)
- [ ] Sistema de postulaciones usando portafolios como carta de presentación
- [ ] Filtros de ofertas conectados a catálogos normalizados
- [ ] Validaciones de postulaciones (duplicidad, cupos)
- [ ] Notificaciones básicas por email
- [ ] Panel de gestión para empleadores

**Base sólida construida en Sprints 1-2:**

- ✅ Sistema de usuarios autenticados y diferenciados
- ✅ Portafolios profesionales como vitrina pública
- ✅ Catálogos normalizados para filtros inteligentes
- ✅ Búsqueda avanzada adaptable a ofertas
- ✅ Arquitectura escalable y mantenible alineado con los objetivos, los requerimientos del MVP y las convenciones de este repositorio.

---

## 1) Resumen del proyecto

**Meet & Gig** es una plataforma web que conecta músicos profesionales con empleadores del rubro musical (locales, bares, productores de eventos). El sistema prioriza la **visibilidad pública del portafolio del músico** como “vitrina” y flujos simples de publicación y postulación a ofertas.

- **Stack**: Django (backend, arquitectura limpia), HTML/CSS/JS en primer término, con vistas server-side; base de datos relacional.
- **Rol**: proyecto desarrollado por 1 persona, con enfoque ágil (Scrum).
- **Entidades principales (alto nivel)**: Usuario, PerfilMúsico, PerfilEmpleador, Portafolio, OfertaLaboral, Postulación, Testimonio/Referencia, Multimedia del Portafolio, Catálogos (Instrumento, Género, Nivel, Ubicación, etc.).

---

## 2) Objetivos

1. Permitir que **músicos creen y publiquen un portafolio profesional** accesible públicamente con información curada y multimedia.
2. Habilitar a **empleadores** a **publicar ofertas** y evaluar músicos mediante su **portafolio**.
3. Soportar **búsqueda/filtrado** por criterios simples (instrumento, género, ubicación, experiencia), basados en **categorías normalizadas**.
4. Proveer flujos mínimos de **postulación**, **referencias** y **moderación** para el MVP.
5. Mantener el código **limpio, DRY y seguro**, con separación clara entre **perfil interno** y **portafolio público**.

---

## 3) Alcance del MVP (derivado de tickets)

**✅ SPRINT 1 - COMPLETADO:** Autenticación y acceso básico (6 tickets completados)

- 1.1: Registro de usuario ✅
- 1.2: Inicio de sesión ✅
- 1.3: Cierre de sesión ✅
- 1.4: Recuperación de contraseña ✅
- 1.5: Acceso al panel de administración ✅
- 1.6: Diseño de la pantalla de login ✅

**✅ SPRINT 2 - COMPLETADO:** Perfiles de usuario (9 tickets - 7 completados, 2 pendientes)

- 2.1: Crear y editar perfil de músico ✅
- 2.2: Crear y editar perfil de empleador ✅
- 2.3: Subida de foto de perfil ✅
- 2.4: Vista del portafolio del músico ✅
- 2.5: Crear y editar contenido del portafolio ✅
- 2.6: Diseño de pantallas de perfil 🔄 PENDIENTE
- 2.7: Validación de unicidad de perfil ✅
- 2.8: Búsqueda y listado de portafolios ✅
- 2.9: Normalización de categorías en portafolio ✅

**🔄 SPRINT 3:** Publicación y ofertas laborales (7 tickets planificados)
**🔄 SPRINT 4:** Referencias, visualización y moderación (9 tickets planificados)

---

## 4) Requerimientos funcionales (MVP)

1. **Autenticación**: registro, login/logout, recuperación por email, admin para superusuarios.
2. **Perfiles**: un usuario puede ser **músico** o **empleador**; se crea/edita su perfil correspondiente.
3. **Portafolio de músico**:
   - CRUD de contenido profesional (**instrumentos, géneros, experiencia, biografía**, enlaces externos).
   - **Vista pública profesional** con diseño responsive e integración completa.
   - **Búsqueda y filtrado público** por criterios múltiples (instrumentos, géneros, ubicación).
   - **Catálogos normalizados**: 63 instrumentos, 28 géneros, ubicaciones chilenas.
   - **Configuración de visibilidad** por campo o sección.
   - **Unicidad**: un usuario músico tiene **exactamente un** portafolio asociado.
   - **URLs SEO-friendly** (`/portafolio/<username>/`) accesible públicamente.
4. **Búsqueda y exploración pública** de portafolios por **instrumento, género, ubicación y/o experiencia**, dependiente de **categorías normalizadas**.
5. **Ofertas laborales**: empleadores crean y publican ofertas; músicos **postulan con su portafolio** (no con el perfil interno).
6. **Moderación/Administración**: edición/bloqueo/eliminación básica de usuarios, ofertas y portafolios ante mal uso; notificaciones mínimas de postulación/resultado.
7. **Diseño responsive** para vistas clave (login, perfiles, portafolio público, listados de ofertas).

---

## 5) Requerimientos no funcionales

- **Código**: limpio, **DRY**, modular; principio de responsabilidad única; pruebas mínimas en modelos/servicios críticos.
- **Seguridad**: validación de inputs, CSRF activo, autenticación estándar de Django, roles básicos (músico/empleador/admin). No exponer emails si el usuario lo marcó como privado.
- **Datos**: normalización de categorías (Instrumento, Género, Nivel, Ubicación) para filtros consistentes; unicidad de portafolio por usuario; slugs legibles.
- **Rendimiento**: consultas eficientes en listados públicos de portafolios/ofertas (prefetch/select_related donde aplique); paginación server-side.
- **UX**: formularios claros; feedback de validaciones; mensajes de éxito/error; accesibilidad básica.
- **Mantenibilidad**: arquitectura limpia, separación de capas (dominio/servicios/repositorios/vistas); límites de tamaño de archivo; reutilización de templates (base para perfiles); centralizar CSS común.
- **Cumplimiento de lineamientos internos**: seguir estrictamente el archivo **guidelines.md** del repo (estilo, DRY, errores, PF, etc.).

---

## 6) Decisiones de diseño clave (perfil vs portafolio)

- **Separación**: `PerfilMusico` almacena **datos personales/administrativos** (p.ej., nombre público, ubicación base, foto de perfil). `Portafolio` contiene **solo información profesional pública**.
- **Sin duplicación**: ningún campo profesional debe duplicarse en `PerfilMusico`. Si hoy existe, **migrar** al modelo `Portafolio` y eliminar en el perfil.
- **Seed/Sincronización controlada**: al crear un `Portafolio` por primera vez, **sembrar** datos iniciales desde el perfil (solo si existen) mediante un **servicio de dominio** (no en la vista). No mantener sincronización automática bidireccional para evitar estados confusos; el **portafolio es la fuente de verdad** de lo público.
- **Visibilidad**: agregar **flags de visibilidad** por campo/sección en `Portafolio` (p.ej., `show_email`, `show_social_links`, `show_education`, etc.). Defaults conservadores (privado), con opt-in explícito.
- **Slug público**: `Portfolio.slug` único y estable para URL pública (`/p/<slug>/`). Evitar exponer IDs incrementales en URLs públicas.
- **Categorías normalizadas**: `Instrumento`, `Genero`, `NivelExperiencia`, `Ubicacion` como catálogos (tablas) con **choices** o FK. Esto es prerequisito para la **búsqueda (2.10)**.

---

## 7) Aceptación para resolver el problema actual (2.4 y 2.5)

### 2.4 — Crear/editar contenido del portafolio

- **Dado** un músico autenticado **y** un portafolio existente (autocreado al completar perfil o al acceder por primera vez),
- **Cuando** edita secciones profesionales (bio, instrumentos*, géneros*, nivel\*, formación, enlaces, multimedia\*\*),
- **Entonces** persiste en el modelo `Portafolio` y entidades relacionadas (`PortfolioInstrumento`, `PortfolioGenero`, etc.).
- **Y** se respetan flags de visibilidad por sección/campo.
- **Y** validaciones: máximo de elementos por sección (p.ej. hasta 5 géneros, 3 instrumentos principales), enlaces válidos, tamaños de imagen acotados.
- **Notas**: (\* categorías normalizadas), (\*\* multimedia como imágenes y URLs a YouTube/SoundCloud).

### 2.5 — Vista del portafolio profesional público

- **URL pública** `/p/<slug>/` accesible sin login.
- **Muestra**: nombre artístico, foto, bio, instrumentos/géneros/nivel normalizados, formación, multimedia, testimonios, **contacto** condicionado por flags (`show_email`, `show_social_links`).
- **SEO mínimo**: `<title>` con nombre artístico + “Portafolio | Meet & Gig”; meta description breve.
- **Rendimiento**: prefetch/select_related para cargar relaciones; paginación de multimedia si excede N items.
- **Diseño**: responsive; plantilla dedicada `portfolio_public.html`; componentes reutilizables.

---

## 8) Modelo de datos (borrador de referencia para guiar a Copilot)

- `Usuario(AbstractUser)`
- `PerfilMusico(user OneToOne)` → datos personales/administrativos básicos (NO campos profesionales).
- `PerfilEmpleador(user OneToOne)`
- `Portafolio(user OneToOne, slug unique)` → bio, flags de visibilidad, FK a catálogos y M2M a tablas intermedias.
- Catálogos: `Instrumento`, `Genero`, `NivelExperiencia`, `Ubicacion`.
- Vínculos: `PortfolioInstrumento(Portafolio, Instrumento, prioridad)`, `PortfolioGenero(Portafolio, Genero)`, etc.
- `Multimedia(Portafolio, tipo, url|image, orden)`
- `Testimonio(Portafolio, autor_nombre|usuario_opcional, texto, fecha_publicacion, verificado_bool)`
- Ofertas/Postulaciones en Sprints 3–4.

> **Nota:** Copilot debe **proponer migraciones** que muevan campos profesionales de `PerfilMusico` hacia `Portafolio` y actualicen formularios/vistas, **sin duplicación**.

---

## 9) Rutas mínimas (MVP)

- `/perfil/musico/editar/`
- `/portafolio/editar/` (solo dueño)
- `/p/<slug>/` (público)
- `/portafolios/` — listado/búsqueda pública (paginado, con filtros por catálogos)
- `/ofertas/` — listado público; `/ofertas/nueva/` (empleador); `/ofertas/<id>/` (detalle)

---

## 10) Convenciones y estilo **(obligatorio)**

- Seguir **guidelines.md** del repo: precisión, cambios quirúrgicos, DRY, nombres expresivos, manejo correcto de errores, seguridad, y Programación Funcional (puras, inmutabilidad, composición, declarativo).
- Evitar scripts one-off en el repo; no dejar TODOs; mantener archivos < 200 LOC; centralizar CSS y templates base compartidos (perfiles/portafolios).
- Implementar pruebas unitarias mínimas en modelos/servicios de Portafolio y búsqueda.
- No introducir nuevas libs/patrones sin justificar y **refactorizar** lo anterior.

---

## 11) Estado actual y prioridades inmediatas

- **Estado**: ✅ **Sprint 1 y Sprint 2 COMPLETADOS** - Sistema de autenticación y portafolios profesionales funcionales
- **Progreso MVP**: **50% completado** (2/4 sprints terminados)
- **Funcionalidades activas**: Registro, login, perfiles diferenciados, portafolios públicos, búsqueda avanzada, catálogos poblados
- **Prioridad**: Planificación y desarrollo del **Sprint 3** (sistema de ofertas laborales)
- **Documentación**: Sprint 1 y 2 completamente documentados, tickets validados

---

## 12) Guía para Copilot (qué sugerir)

1. **Migraciones** que eliminen campos profesionales de `PerfilMusico` y los creen en `Portafolio` + tablas relacionales normalizadas.
2. **Servicios de dominio** para: crear/sembrar Portafolio; agregar/quitar instrumentos/géneros; validar límites; componer DTOs para vistas públicas.
3. **Forms y Views**: `PortfolioEditForm`, `PortfolioPublicView(slug)` con prefetch; `PortfolioSearchView` con filtros sobre catálogos.
4. **Templates**: `portfolio_edit.html`, `portfolio_public.html`; componentes parciales reutilizables; template base para perfiles.
5. **Tests**: unicidad de portafolio, creación de slug, visibilidad de campos, filtros de búsqueda.

---

## 13) Checklist de “hecho” (Definition of Done) para 2.4/2.5

- No hay campos profesionales en `PerfilMusico`.
- Existe `Portafolio` OneToOne con `Usuario` (o Perfil), con `slug` único.
- Form de edición guarda y valida categorías normalizadas y flags de visibilidad.
- Vista pública carga en ≤150 ms en dev y ≤ N consultas SQL con `prefetch_related`.
- Pruebas básicas pasan (crear portafolio, visibilidad, filtros simples).
- Sin duplicación de templates/CSS (usa base común).

---

### Notas finales para Copilot

- **No asumas sincronización automática** entre Perfil y Portafolio más allá del “seed” inicial controlado: la edición pública sucede en `Portafolio`.
- **Prioriza (2.11) Normalización** antes de implementar filtros complejos de (2.10).
- Revisa `guidelines.md` para estilo, seguridad y PF antes de sugerir cambios.
