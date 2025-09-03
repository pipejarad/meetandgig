# 📋 Backlog de Desarrollo - Meet & Gig (MVP)

## 🟩 Sprint 1: Autenticación y Acceso Básico

| Ticket | Título                            | Estado        | Descripción breve                                    |
| ------ | --------------------------------- | ------------- | ---------------------------------------------------- |
| 1.1    | Registro de usuario               | ✅ COMPLETADO | Registro con validación de email único y contraseña. |
| 1.2    | Inicio de sesión                  | ✅ COMPLETADO | Validación de credenciales y persistencia de sesión. |
| 1.3    | Cierre de sesión                  | ✅ COMPLETADO | Destruye sesión y redirige al login.                 |
| 1.4    | Recuperación de contraseña        | ✅ COMPLETADO | Envío de enlace por correo.                          |
| 1.5    | Acceso al panel de administración | ✅ COMPLETADO | Permite acceso a Django admin para superusuarios.    |
| 1.6    | Diseño de la pantalla de login    | ✅ COMPLETADO | UI responsiva y amigable para login.                 |

---

## 🟩 Sprint 2: Perfiles de Usuario

| Ticket | Título                                    | Estado        | Descripción                                                                                                                                                                                                                                                          |
| ------ | ----------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.1    | Crear y editar perfil de músico           | ✅ COMPLETADO | Perfil administrativo/personal del músico. Datos profesionales migrados al modelo Portafolio.                                                                                                                                                                        |
| 2.2    | Crear y editar perfil de empleador        | ✅ HECHO      | Formulario para datos de empleador (organización, contacto, etc.).                                                                                                                                                                                                   |
| 2.3    | Subida de foto de perfil                  | ✅ HECHO      | Carga y visualización de imagen para perfiles.                                                                                                                                                                                                                       |
| 2.4    | Vista del portafolio del músico           | ✅ COMPLETADO | Página pública que muestra la biografía, instrumentos, géneros, experiencia musical, material multimedia y referencias del músico. Esta vista actúa como su presentación profesional ante empleadores. Incluye diseño responsivo e integración con datos del perfil. |
| 2.5    | Crear y editar contenido del portafolio   | ✅ COMPLETADO | Formulario para que músicos gestionen su información profesional: instrumentos, géneros, experiencia musical, enlaces externos, formación, y secciones multimedia para construir su portafolio profesional.                                                          |
| 2.6    | Diseño de pantallas de perfil             | ✅ COMPLETADO | Diseño responsivo para perfiles según tipo de usuario (privados/administrativos). **INCLUYE:** Ruta `/p/<slug>/` y SEO básico para portafolios.                                                                                                                      |
| 2.7    | Validación de unicidad de perfil          | ✅ HECHO      | Lógica para que un usuario tenga un solo perfil y un solo portafolio.                                                                                                                                                                                                |
| 🔥 2.8 | Búsqueda y listado de portafolios         | ✅ COMPLETADO | Sistema completo de búsqueda y filtrado de músicos. Incluye filtros por instrumentos, géneros, ubicación, experiencia, formación y palabras clave.                                                                                                                   |
| 🔥 2.9 | Normalización de categorías en portafolio | ✅ COMPLETADO | Catálogos poblados con 63 instrumentos, 28 géneros, ubicaciones chilenas. Management command, admin interface mejorado y tests implementados.                                                                                                                        |

---

## 🟩 Sprint 3: Publicación y Ofertas Laborales

| Ticket | Título                                 | Estado        | Descripción breve                                                                                                                                |
| ------ | -------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| 🔥 3.1 | Crear oferta laboral                   | ✅ COMPLETADO | Formulario completo para empleadores con integración de catálogos, validaciones y navegación.                                                    |
| 3.2    | Visualizar ofertas publicadas          | ✅ COMPLETADO | Listado público de ofertas con diseño responsivo y paginación.                                                                                   |
| 🔥 3.3 | Filtrar ofertas por criterios          | ✅ COMPLETADO | Filtros múltiples por instrumentos, géneros, ubicación, presupuesto, fechas y ordenamiento.                                                      |
| 3.4    | Cerrar oferta laboral                  | ✅ COMPLETADO | Sistema completo de cierre/reapertura con validaciones y confirmaciones.                                                                         |
| 3.5    | Diseño de vista de ofertas             | ✅ COMPLETADO | UI responsive para navegación de ofertas - Mobile-first con offcanvas, acordeones y sincronización.                                              |
| 🔥 3.6 | Postulación a una oferta laboral       | ✅ COMPLETADO | Sistema completo de postulaciones: formulario con validaciones, sidebar dinámico, estados visuales y experiencia optimizada por tipo de usuario. |
| 🔥 3.7 | Validaciones de postulaciones y cierre | ✅ COMPLETADO | Sistema completo de validaciones, gestión de postulaciones, cancelación y notificaciones automáticas.                                            |
| 🔥 3.8 | Invitación directa a músicos           | ✅ COMPLETADO | Sistema completo de invitaciones directas con dashboard para músicos, gestión para empleadores y notificaciones automáticas.                     |

---

## 🟩 Sprint 4: Visualización, Referencias y Moderación

| Ticket | Título                                       | Estado        | Descripción breve                                        |
| ------ | -------------------------------------------- | ------------- | -------------------------------------------------------- |
| 4.1    | Agregar referencia laboral                   | ✅ COMPLETADO | Sistema completo de referencias con modelo Testimonio, forms de solicitud/respuesta y workflow de aprobación. |
| 4.2    | Visualizar referencias laborales             | ✅ COMPLETADO | Referencias integradas en portafolio con sistema de tokens para solicitudes seguras. |
| 4.3    | Mostrar información de contacto              | ✅ COMPLETADO | Email de contacto incluido en sistema de notificaciones y templates. |
| 4.4    | Notificar postulación a empleador            | ✅ COMPLETADO | Sistema completo de notificaciones por email con templates HTML/texto profesionales. |
| 4.5    | Notificar resultado de postulación al músico | ✅ COMPLETADO | Notificaciones automáticas para aceptación/rechazo con URLs corregidas. |
| 4.6    | Revisar y aceptar/rechazar postulaciones     | 🔶 PARCIAL    | Funcionalidad básica via admin. Pendiente: dashboard dedicado para empleadores. |
| 4.7    | Vista de estado de postulación               | 🔶 PARCIAL    | Vista `mis_postulaciones` con estadísticas básicas. Pendiente: dashboard mejorado. |
| 4.8    | Funcionalidad de moderación básica           | ✅ COMPLETADO | Admin interface mejorado con filtros, acciones en lote y correcciones de campos. |
| 4.9    | Diseño responsive general                    | 🔍 PENDIENTE  | Requiere evaluación y audit de responsive design en toda la aplicación. |

---

## 📊 Resumen de Progreso por Sprint

- **Sprint 1**: ✅ 100% Completado (6/6 tickets)
- **Sprint 2**: ✅ 100% Completado (9/9 tickets)  
- **Sprint 3**: ✅ 100% Completado (8/8 tickets)
- **Sprint 4**: 🔶 ~80% Completado (6/9 tickets completos, 2 parciales, 1 pendiente)

---

**🔥 = Ticket crítico agregado para completar cobertura del MVP**
