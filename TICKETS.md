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
| 2.6    | Diseño de pantallas de perfil             | 🔄 PENDIENTE  | Diseño responsivo para perfiles según tipo de usuario (privados/administrativos). **INCLUYE:** Ruta `/p/<slug>/` y SEO básico para portafolios.                                                                                                                      |
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
| 🔥 3.7 | Validaciones de postulaciones y cierre | 🔄 PENDIENTE  | Reglas para evitar duplicidad, control de cupos, cierre.                                                                                         |
| 🔥 3.8 | Invitación directa a músicos           | 🔄 PENDIENTE  | Empleadores pueden invitar músicos específicos desde portafolios a ofertas existentes.                                                           |

---

## 🟩 Sprint 4: Visualización, Referencias y Moderación

| Ticket | Título                                       | Descripción breve                                        |
| ------ | -------------------------------------------- | -------------------------------------------------------- |
| 4.1    | Agregar referencia laboral                   | Permitir agregar referencias al portafolio de un músico. |
| 4.2    | Visualizar referencias laborales             | Las referencias son visibles en el portafolio.           |
| 4.3    | Mostrar información de contacto              | Email u otros datos visibles según configuración.        |
| 4.4    | Notificar postulación a empleador            | Email o alerta al recibir nueva postulación.             |
| 4.5    | Notificar resultado de postulación al músico | Notificación si es aceptado o rechazado.                 |
| 4.6    | Revisar y aceptar/rechazar postulaciones     | Gestión de candidaturas por parte del empleador.         |
| 4.7    | Vista de estado de postulación               | Músico puede ver estado de sus postulaciones.            |
| 4.8    | Funcionalidad de moderación básica           | Admin puede editar/eliminar usuarios, ofertas, etc.      |
| 4.9    | Diseño responsive general                    | Garantizar experiencia óptima en móvil/escritorio.       |

---

**🔥 = Ticket crítico agregado para completar cobertura del MVP**
