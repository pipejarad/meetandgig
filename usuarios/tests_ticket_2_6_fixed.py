"""
Tests simplificados para Ticket 2.6 - URLs públicos y SEO básico
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from usuarios.models import Portafolio, NivelExperiencia, Ubicacion

Usuario = get_user_model()


class PortafolioPublicoBasicTestCase(TestCase):
    """Tests básicos para el portafolio público - sin modelos managed=False"""
    
    def setUp(self):
        # Crear objetos dependientes primero
        self.nivel_experiencia = NivelExperiencia.objects.create(
            nombre='Intermedio',
            descripcion='Músico con experiencia',
            orden=2,
            años_minimos=3,
            años_maximos=10
        )
        
        self.ubicacion = Ubicacion.objects.create(
            nombre='Santiago',
            region='Metropolitana',
            pais='Chile',
            activo=True,
            orden=1
        )
        
        # Crear usuario básico
        self.usuario = Usuario.objects.create_user(
            username='testmusico',
            email='test@example.com',
            first_name='Test',
            last_name='Musician'
        )
        
        # Crear portafolio básico - usando objetos relacionados
        self.portafolio = Portafolio.objects.create(
            usuario=self.usuario,
            slug='test-musician',
            biografia='Biografía de prueba para testing',
            años_experiencia=5,
            nivel_experiencia=self.nivel_experiencia,
            ubicacion=self.ubicacion,
            tarifa_base=50000,
            disponible_para_gigs=True,
            activo=True,
            website_personal='https://testmusician.com',
            youtube_url='https://youtube.com/testmusician',
            instagram_url='https://instagram.com/testmusician'
        )
    
    def test_portafolio_publico_url_funciona(self):
        """Test que la URL pública del portafolio funciona correctamente"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_portafolio_publico_sin_autenticacion(self):
        """Test que el portafolio público es accesible sin autenticación"""
        # Asegurar que no hay usuario autenticado
        self.client.logout()
        
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_portafolio_publico_contenido_basico(self):
        """Test que el portafolio público muestra el contenido básico"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        # Verificar que el contenido básico está presente
        self.assertContains(response, 'Test Musician')
        self.assertContains(response, 'Santiago')
        self.assertContains(response, 'Biografía de prueba para testing')
        self.assertContains(response, '5 años de experiencia')

    def test_portafolio_inexistente_404(self):
        """Test que un slug inexistente devuelve 404"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': 'inexistente'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_seo_meta_tags_presentes(self):
        """Test que los meta tags de SEO están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        # Verificar meta tags básicos
        self.assertContains(response, '<meta name="description"')
        self.assertContains(response, '<meta name="keywords"')
        self.assertContains(response, '<link rel="canonical"')

    def test_open_graph_tags_presentes(self):
        """Test que los tags de Open Graph están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        # Verificar Open Graph tags
        self.assertContains(response, 'property="og:title"')
        self.assertContains(response, 'property="og:description"')
        self.assertContains(response, 'property="og:type"')
        self.assertContains(response, 'property="og:url"')

    def test_structured_data_presente(self):
        """Test que los datos estructurados (Schema.org) están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        # Verificar que hay JSON-LD estructurado
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, '"@type": "Person"')

    def test_enlaces_sociales_visibles_cuando_existen(self):
        """Test que los enlaces sociales se muestran cuando están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        # Verificar que los enlaces sociales aparecen
        self.assertContains(response, 'https://youtube.com/testmusician')
        self.assertContains(response, 'https://instagram.com/testmusician')
        self.assertContains(response, 'https://testmusician.com')

    def test_botones_compartir_presentes(self):
        """Test que los botones de compartir están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        # Verificar que hay botones de compartir
        self.assertContains(response, 'Compartir en Facebook')
        self.assertContains(response, 'Compartir en Twitter')
        self.assertContains(response, 'Compartir en WhatsApp')


class IntegracionUrlsBasicTestCase(TestCase):
    """Tests de integración para validar que las URLs funcionan independientemente"""
    
    def setUp(self):
        # Crear objetos dependientes
        self.nivel_experiencia = NivelExperiencia.objects.create(
            nombre='Avanzado',
            descripcion='Músico profesional',
            orden=3,
            años_minimos=10
        )
        
        self.ubicacion = Ubicacion.objects.create(
            nombre='Valparaíso',
            region='Valparaíso',
            pais='Chile',
            activo=True,
            orden=2
        )
        
        self.usuario = Usuario.objects.create_user(
            username='musico_avanzado',
            email='avanzado@example.com',
            first_name='María',
            last_name='López'
        )
        
        self.portafolio = Portafolio.objects.create(
            usuario=self.usuario,
            slug='maria-lopez-violinista',
            biografia='Violinista profesional con 15 años de experiencia',
            años_experiencia=15,
            nivel_experiencia=self.nivel_experiencia,
            ubicacion=self.ubicacion,
            tarifa_base=100000,
            disponible_para_gigs=True,
            activo=True
        )

    def test_nueva_url_funciona_independientemente(self):
        """Test que la nueva URL funciona de forma independiente"""
        # Test directo de la URL
        response = self.client.get(f'/usuarios/p/{self.portafolio.slug}/')
        self.assertEqual(response.status_code, 200)
        
        # Test usando reverse
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que contiene información correcta
        self.assertContains(response, 'María López')
        self.assertContains(response, 'Violinista profesional')
        self.assertContains(response, '15 años de experiencia')
