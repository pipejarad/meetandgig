# 🎯 PLAN TICKET 2.6 - Diseño de pantallas de perfil (FINALIZAR SPRINT 2)

## 📋 Estado Actual: ANÁLISIS Y PLANIFICACIÓN

**Objetivo**: Completar el último ticket del Sprint 2 para alcanzar el 100% de funcionalidad
**Scope**: URLs públicas, SEO básico, mejoras visuales finales
**Impacto**: Portafolios completamente públicos y optimizados para búsqueda

---

## 🎯 **ANÁLISIS TÉCNICO DETALLADO**

### **Componentes a Implementar**

#### **1. RUTAS PÚBLICAS `/p/<slug>/`**

**Implementación requerida**:

```python
# usuarios/urls.py - Agregar nueva ruta
path('p/<slug:slug>/', views.PortafolioPublicoView.as_view(), name='portafolio_publico'),

# usuarios/views.py - Nueva vista pública
class PortafolioPublicoView(DetailView):
    model = Portafolio
    template_name = 'usuarios/portafolio_publico.html'
    slug_field = 'slug'
    context_object_name = 'portafolio'
```

**Requisitos técnicos**:

- ✅ **Campo slug ya existe** en modelo Portafolio
- ✅ **Auto-generación** de slug desde nombre artístico
- 🔄 **Vista pública** sin autenticación requerida
- 🔄 **Template optimizado** para SEO y sharing

#### **2. SEO BÁSICO PARA PORTAFOLIOS**

**Meta Tags Dinámicos**:

```html
<!-- Template: portafolio_publico.html -->
<head>
  <title>{{ portafolio.nombre_artistico }} - Músico en Meet&Gig</title>
  <meta
    name="description"
    content="{{ portafolio.biografia|truncatewords:25 }}"
  />
  <meta
    name="keywords"
    content="{{ portafolio.instrumentos_nombres }}, {{ portafolio.generos_nombres }}, músico {{ portafolio.ubicacion }}"
  />

  <!-- Open Graph para redes sociales -->
  <meta
    property="og:title"
    content="{{ portafolio.nombre_artistico }} - Músico Profesional"
  />
  <meta
    property="og:description"
    content="{{ portafolio.biografia|truncatewords:20 }}"
  />
  <meta
    property="og:image"
    content="{{ portafolio.perfil_musico.foto_perfil.url }}"
  />
  <meta property="og:url" content="{{ request.build_absolute_uri }}" />

  <!-- Schema.org para Google -->
  <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "{{ portafolio.nombre_artistico }}",
      "description": "{{ portafolio.biografia|truncatewords:25 }}",
      "image": "{{ portafolio.perfil_musico.foto_perfil.url }}",
      "jobTitle": "Músico",
      "worksFor": {
        "@type": "Organization",
        "name": "Meet&Gig"
      }
    }
  </script>
</head>
```

#### **3. MEJORAS VISUALES Y UI/UX**

**Template Público Optimizado**:

- **Header atractivo** con foto, nombre artístico y ubicación
- **Sección de instrumentos** con iconos visuales
- **Géneros musicales** con badges coloridos
- **Enlaces sociales** prominentes y funcionales
- **Call-to-action** para contactar al músico
- **Breadcrumbs** para navegación
- **Botones de compartir** en redes sociales

---

## 🏗️ **PLAN DE IMPLEMENTACIÓN**

### **FASE 1: URLs y Vista Pública (30 min)**

#### **1.1. Actualizar URLs**

```python
# usuarios/urls.py
urlpatterns = [
    # ... URLs existentes ...
    path('p/<slug:slug>/', views.PortafolioPublicoView.as_view(), name='portafolio_publico'),
]
```

#### **1.2. Crear Vista Pública**

```python
# usuarios/views.py
class PortafolioPublicoView(DetailView):
    model = Portafolio
    template_name = 'usuarios/portafolio_publico.html'
    slug_field = 'slug'
    context_object_name = 'portafolio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portafolio = self.get_object()

        # SEO data
        context['seo_title'] = f"{portafolio.nombre_artistico} - Músico en Meet&Gig"
        context['seo_description'] = portafolio.biografia[:160] if portafolio.biografia else "Músico profesional en Meet&Gig"
        context['seo_keywords'] = self._generate_keywords(portafolio)
        context['canonical_url'] = self.request.build_absolute_uri()

        return context

    def _generate_keywords(self, portafolio):
        keywords = []
        keywords.extend([inst.nombre for inst in portafolio.instrumentos.all()])
        keywords.extend([gen.nombre for gen in portafolio.generos.all()])
        keywords.append(f"músico {portafolio.ubicacion}")
        return ", ".join(keywords[:10])  # Limitar a 10 keywords
```

### **FASE 2: Template Público con SEO (45 min)**

#### **2.1. Crear Template Base SEO**

```html
<!-- usuarios/templates/usuarios/portafolio_publico.html -->
{% extends "base.html" %} {% load static %} {% block title %}{{ seo_title }}{%
endblock %} {% block extra_head %}
<!-- SEO Meta Tags -->
<meta name="description" content="{{ seo_description }}" />
<meta name="keywords" content="{{ seo_keywords }}" />
<meta name="author" content="{{ portafolio.nombre_artistico }}" />
<link rel="canonical" href="{{ canonical_url }}" />

<!-- Open Graph -->
<meta property="og:title" content="{{ seo_title }}" />
<meta property="og:description" content="{{ seo_description }}" />
{% if portafolio.perfil_musico.foto_perfil %}
<meta
  property="og:image"
  content="{{ request.scheme }}://{{ request.get_host }}{{ portafolio.perfil_musico.foto_perfil.url }}"
/>
{% endif %}
<meta property="og:url" content="{{ canonical_url }}" />
<meta property="og:type" content="profile" />

<!-- Twitter Cards -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{{ seo_title }}" />
<meta name="twitter:description" content="{{ seo_description }}" />

<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
  {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": "{{ portafolio.nombre_artistico }}",
      "description": "{{ seo_description }}",
      {% if portafolio.perfil_musico.foto_perfil %}
      "image": "{{ request.scheme }}://{{ request.get_host }}{{ portafolio.perfil_musico.foto_perfil.url }}",
      {% endif %}
      "jobTitle": "Músico",
      "address": {
          "@type": "PostalAddress",
          "addressLocality": "{{ portafolio.ubicacion }}"
      }
  }
</script>
{% endblock %} {% block content %}
<!-- Contenido del portafolio público optimizado -->
{% endblock %}
```

### **FASE 3: Diseño Visual Avanzado (60 min)**

#### **3.1. Header Atractivo**

```html
<!-- Header del portafolio -->
<div class="hero-section bg-gradient-primary text-white py-5">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-md-3 text-center">
        {% if portafolio.perfil_musico.foto_perfil %}
        <img
          src="{{ portafolio.perfil_musico.foto_perfil.url }}"
          alt="{{ portafolio.nombre_artistico }}"
          class="img-fluid rounded-circle shadow-lg mb-3"
          style="width: 150px; height: 150px; object-fit: cover;"
        />
        {% endif %}
      </div>
      <div class="col-md-9">
        <h1 class="display-4 mb-2">{{ portafolio.nombre_artistico }}</h1>
        <p class="lead mb-3">
          <i class="fas fa-map-marker-alt"></i> {{ portafolio.ubicacion }} {% if
          portafolio.anos_experiencia %} | <i class="fas fa-clock"></i> {{
          portafolio.anos_experiencia }} años de experiencia {% endif %}
        </p>
        <div class="d-flex flex-wrap gap-2">
          {% for instrumento in portafolio.instrumentos.all|slice:":5" %}
          <span class="badge badge-light badge-lg">
            <i class="fas fa-music"></i> {{ instrumento.nombre }}
          </span>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
</div>
```

#### **3.2. Secciones Organizadas**

```html
<!-- Navegación de secciones -->
<div class="container mt-4">
  <nav class="navbar navbar-expand-lg navbar-light bg-light rounded">
    <div class="navbar-nav mx-auto">
      <a class="nav-link" href="#biografia">Biografía</a>
      <a class="nav-link" href="#instrumentos">Instrumentos</a>
      <a class="nav-link" href="#generos">Géneros</a>
      <a class="nav-link" href="#formacion">Formación</a>
      <a class="nav-link" href="#enlaces">Enlaces</a>
      <a class="nav-link" href="#contacto">Contacto</a>
    </div>
  </nav>
</div>

<!-- Contenido por secciones -->
<div class="container my-5">
  <div class="row">
    <div class="col-md-8">
      <!-- Biografía -->
      <section id="biografia" class="mb-5">
        <h3><i class="fas fa-user-circle"></i> Biografía</h3>
        <div class="card">
          <div class="card-body">
            <p class="card-text">{{ portafolio.biografia|linebreaks }}</p>
          </div>
        </div>
      </section>

      <!-- Instrumentos con iconos -->
      <section id="instrumentos" class="mb-5">
        <h3><i class="fas fa-guitar"></i> Instrumentos</h3>
        <div class="row">
          {% for instrumento in portafolio.instrumentos.all %}
          <div class="col-md-6 mb-3">
            <div class="card h-100">
              <div class="card-body text-center">
                <i class="fas fa-music fa-2x text-primary mb-2"></i>
                <h5>{{ instrumento.nombre }}</h5>
                <span class="badge badge-secondary"
                  >{{ instrumento.categoria }}</span
                >
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </section>
    </div>

    <div class="col-md-4">
      <!-- Sidebar con info adicional -->
      <aside class="sticky-top">
        <!-- Enlaces sociales -->
        <div class="card mb-4">
          <div class="card-header">
            <h5><i class="fas fa-share-alt"></i> Enlaces</h5>
          </div>
          <div class="card-body">
            {% if portafolio.youtube_url %}
            <a
              href="{{ portafolio.youtube_url }}"
              class="btn btn-danger btn-block mb-2"
              target="_blank"
            >
              <i class="fab fa-youtube"></i> YouTube
            </a>
            {% endif %} {% if portafolio.spotify_url %}
            <a
              href="{{ portafolio.spotify_url }}"
              class="btn btn-success btn-block mb-2"
              target="_blank"
            >
              <i class="fab fa-spotify"></i> Spotify
            </a>
            {% endif %}
            <!-- Más enlaces sociales -->
          </div>
        </div>

        <!-- Call to action -->
        <div class="card">
          <div class="card-body text-center">
            <h5>¿Interesado en contratar?</h5>
            <p>Contacta directamente con {{ portafolio.nombre_artistico }}</p>
            <a
              href="{% url 'usuarios:buscar_portafolios' %}"
              class="btn btn-primary"
            >
              <i class="fas fa-search"></i> Buscar más músicos
            </a>
          </div>
        </div>
      </aside>
    </div>
  </div>
</div>
```

### **FASE 4: Integración y Testing (30 min)**

#### **4.1. Actualizar Enlaces Existentes**

```python
# Actualizar templates existentes para usar nueva URL
# En ver_portafolio_musico.html y buscar_portafolios.html:
<a href="{% url 'usuarios:portafolio_publico' slug=portafolio.slug %}" class="btn btn-primary">
    <i class="fas fa-eye"></i> Ver Portafolio Público
</a>
```

#### **4.2. Tests de SEO y URLs**

```python
# usuarios/tests.py - Agregar tests para nueva funcionalidad
class PortafolioPublicoTestCase(TestCase):
    def test_portafolio_publico_url(self):
        portafolio = self._crear_portafolio_test()
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_seo_meta_tags(self):
        portafolio = self._crear_portafolio_test()
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': portafolio.slug})
        response = self.client.get(url)

        # Verificar meta tags
        self.assertContains(response, f'<title>{portafolio.nombre_artistico}')
        self.assertContains(response, 'meta name="description"')
        self.assertContains(response, 'meta property="og:title"')
        self.assertContains(response, 'application/ld+json')
```

---

## 📊 **IMPACTO Y BENEFICIOS**

### **Para Músicos**:

- ✅ **URLs amigables**: `/p/juan-guitarrista/` más profesional que `/portafolio/123/`
- ✅ **Mejor SEO**: Portafolios indexables por Google con metadatos ricos
- ✅ **Sharing optimizado**: Enlaces bonitos para compartir en redes sociales
- ✅ **Experiencia profesional**: Templates mejorados y más visuales

### **Para Empleadores**:

- ✅ **Acceso directo**: Enlaces públicos compartibles sin autenticación
- ✅ **Información rica**: Structured data para mejor comprensión
- ✅ **Navegación intuitiva**: Secciones organizadas y fácil acceso

### **Para el Sistema**:

- ✅ **SEO mejorado**: Mejor posicionamiento en buscadores
- ✅ **Analytics**: Tracking de visitas a portafolios específicos
- ✅ **Social sharing**: Metadatos optimizados para redes sociales
- ✅ **Professional image**: URLs y diseño más profesional

---

## ⏱️ **CRONOGRAMA DE EJECUCIÓN**

| Fase       | Duración     | Actividades                 |
| ---------- | ------------ | --------------------------- |
| **Fase 1** | 30 min       | URLs y vista pública básica |
| **Fase 2** | 45 min       | Template con SEO completo   |
| **Fase 3** | 60 min       | Diseño visual y UX          |
| **Fase 4** | 30 min       | Testing y integración       |
| **TOTAL**  | **2h 45min** | **TICKET 2.6 COMPLETADO**   |

---

## ✅ **CRITERIOS DE ACEPTACIÓN**

1. ✅ **URL pública funcional**: `/p/<slug>/` accesible sin autenticación
2. ✅ **SEO básico implementado**: Meta tags, Open Graph, Schema.org
3. ✅ **Template optimizado**: Diseño profesional y responsive
4. ✅ **Enlaces sociales**: Prominentes y funcionales
5. ✅ **Tests pasando**: Cobertura de nueva funcionalidad
6. ✅ **Integración completa**: Enlaces actualizados en sistema existente

---

## 🚀 **RESULTADO FINAL**

Al completar este ticket:

### ✅ **SPRINT 2 COMPLETADO AL 100%**

- Todos los tickets (2.1 - 2.9) implementados
- Sistema de perfiles y portafolios completamente funcional
- Base sólida para Sprint 3 (ofertas laborales)

### ✅ **FUNCIONALIDADES FINALES DEL SPRINT 2**:

1. **Perfiles completos**: Músicos y empleadores
2. **Portafolios profesionales**: Con datos normalizados
3. **Sistema de búsqueda**: Con filtros avanzados
4. **Catálogos poblados**: 63 instrumentos, 28 géneros
5. **URLs públicas**: SEO-friendly y compartibles
6. **Admin avanzado**: Con estadísticas y gestión
7. **Tests completos**: Cobertura integral
8. **Documentación**: Completa y actualizada

---

**🎯 OBJETIVO: Completar Sprint 2 en esta sesión para tener base sólida para Sprint 3**

**📋 PRÓXIMO: Con Sprint 2 completo, el Sprint 3 (ofertas laborales) podrá aprovechar todos los catálogos normalizados y el sistema de portafolios optimizado**
