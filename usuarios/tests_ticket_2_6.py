from django.test import TestCase, Client
from django.urls import reverse
from usuarios.models import Usuario, PerfilMusico, Portafolio


class PortafolioPublicoBasicTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Juan',
            last_name='Pérez'
        )
        self.perfil = PerfilMusico.objects.create(
            usuario=self.user,
            telefono='+56912345678',
            direccion='Santiago, Chile'
        )
        
        self.portafolio = Portafolio.objects.create(
            perfil_musico=self.perfil,
            nombre_artistico='Juan Guitarrista',
            biografia='Músico profesional con 10 años de experiencia',
            anos_experiencia=10,
            ubicacion='Santiago',
            disponible=True,
            tarifa_minima=50000
        )

    def test_portafolio_publico_url_funciona(self):
        """Test que la URL pública del portafolio funciona correctamente"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_portafolio_publico_contenido_basico(self):
        """Test que el portafolio público muestra el contenido básico"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        self.assertContains(response, 'Juan Guitarrista')
        self.assertContains(response, 'Santiago')
        self.assertContains(response, '10 años de experiencia')
        self.assertContains(response, 'Músico profesional')

    def test_seo_meta_tags_presentes(self):
        """Test que los meta tags de SEO están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        self.assertContains(response, 'Juan Guitarrista - Músico en Meet&amp;Gig')
        self.assertContains(response, 'meta name="description"')
        self.assertContains(response, 'meta name="keywords"')
        self.assertContains(response, 'link rel="canonical"')

    def test_open_graph_tags_presentes(self):
        """Test que los tags de Open Graph están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        self.assertContains(response, 'meta property="og:title"')
        self.assertContains(response, 'meta property="og:description"')
        self.assertContains(response, 'meta property="og:url"')
        self.assertContains(response, 'meta property="og:type"')

    def test_structured_data_presente(self):
        """Test que los datos estructurados (Schema.org) están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        self.assertContains(response, 'application/ld+json')
        self.assertContains(response, '"@context": "https://schema.org"')
        self.assertContains(response, '"@type": "Person"')

    def test_portafolio_publico_sin_autenticacion(self):
        """Test que el portafolio público es accesible sin autenticación"""
        self.client.logout()
        
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_portafolio_inexistente_404(self):
        """Test que un slug inexistente devuelve 404"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': 'slug-inexistente'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_botones_compartir_presentes(self):
        """Test que los botones de compartir están presentes"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        self.assertContains(response, 'twitter.com/intent/tweet')
        self.assertContains(response, 'facebook.com/sharer')
        self.assertContains(response, 'whatsapp://send')

    def test_enlaces_sociales_visibles_cuando_existen(self):
        """Test que los enlaces sociales se muestran cuando están presentes"""
        self.portafolio.youtube_url = 'https://youtube.com/juanguitarrista'
        self.portafolio.spotify_url = 'https://spotify.com/artist/juan'
        self.portafolio.save()
        
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        
        self.assertContains(response, 'YouTube')
        self.assertContains(response, 'Spotify')
        self.assertContains(response, self.portafolio.youtube_url)
        self.assertContains(response, self.portafolio.spotify_url)


class IntegracionUrlsBasicTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Usuario.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        self.perfil = PerfilMusico.objects.create(
            usuario=self.user,
            telefono='+56912345678'
        )
        self.portafolio = Portafolio.objects.create(
            perfil_musico=self.perfil,
            nombre_artistico='Test Artist'
        )

    def test_nueva_url_funciona_independientemente(self):
        """Test que la nueva URL funciona de forma independiente"""
        url = reverse('usuarios:portafolio_publico', kwargs={'slug': self.portafolio.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Artist')
