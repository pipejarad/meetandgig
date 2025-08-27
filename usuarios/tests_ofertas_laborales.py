"""
Tests para el sistema de ofertas laborales de Sprint 3
"""
import random
from datetime import timedelta
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from usuarios.models import (
    Usuario, PerfilEmpleador, OfertaLaboral, 
    Instrumento, Genero, NivelExperiencia, Ubicacion,
    OfertaInstrumento, OfertaGenero
)

User = get_user_model()


class OfertaLaboralModelTest(TestCase):
    """Tests para el modelo OfertaLaboral"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear catálogos únicos para evitar conflictos
        self.instrumento, _ = Instrumento.objects.get_or_create(
            nombre='Guitarra Test Ofertas',
            defaults={'categoria': 'Cuerda'}
        )
        self.genero, _ = Genero.objects.get_or_create(
            nombre='Rock Test Ofertas',
            defaults={}
        )
        # Usar orden único para evitar conflictos
        orden_unico = random.randint(2000, 9999)
        self.nivel, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Intermedio Test Ofertas {orden_unico}',
            defaults={'orden': orden_unico}
        )
        self.ubicacion, _ = Ubicacion.objects.get_or_create(
            nombre='Santiago Centro Test Ofertas',
            defaults={'region': 'Región Metropolitana'}
        )
        
        # Crear usuario empleador
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_ofertas_test',
            email='empleador_ofertas@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        
        # Crear perfil empleador
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Test Company Ofertas',
            telefono='+56912345678',
            ubicacion=self.ubicacion.nombre
        )
    
    def test_crear_oferta_laboral_basica(self):
        """Test crear oferta laboral básica"""
        oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='guitarrista-evento-test',
            titulo='Guitarrista para evento',
            descripcion='Buscamos guitarrista experimentado',
            tipo_contrato='evento_unico',
            presupuesto_minimo=100000,
            presupuesto_maximo=200000,
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            cupos_disponibles=1,
            estado='borrador'
        )
        
        self.assertEqual(oferta.titulo, 'Guitarrista para evento')
        self.assertEqual(oferta.empleador, self.empleador)
        self.assertEqual(oferta.estado, 'borrador')
        self.assertEqual(oferta.cupos_disponibles, 1)
        self.assertFalse(oferta.esta_vigente())  # Borrador no está vigente
    
    def test_oferta_slug_unico(self):
        """Test que el slug debe ser único"""
        OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='guitarrista-unico',
            titulo='Guitarrista 1',
            descripcion='Descripción 1',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel
        )
        
        # Intentar crear otra oferta con el mismo slug debe fallar
        with self.assertRaises(IntegrityError):
            OfertaLaboral.objects.create(
                empleador=self.empleador,
                slug='guitarrista-unico',
                titulo='Guitarrista 2',
                descripcion='Descripción 2',
                tipo_contrato='evento_unico',
                fecha_evento=timezone.now() + timedelta(days=30),
                ubicacion=self.ubicacion,
                nivel_experiencia_minimo=self.nivel
            )
    
    def test_oferta_vigente_cuando_publicada(self):
        """Test que oferta está vigente cuando está publicada y dentro de fecha límite"""
        oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='guitarrista-vigente',
            titulo='Guitarrista vigente',
            descripcion='Oferta vigente',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            estado='publicada',
            fecha_limite_postulacion=timezone.now() + timedelta(days=15)
        )
        
        self.assertTrue(oferta.esta_vigente())
    
    def test_oferta_no_vigente_cuando_expirada(self):
        """Test que oferta no está vigente cuando ha expirado"""
        oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='guitarrista-expirada',
            titulo='Guitarrista expirada',
            descripcion='Oferta expirada',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            estado='publicada',
            fecha_limite_postulacion=timezone.now() - timedelta(days=1)  # Expirada
        )
        
        self.assertFalse(oferta.esta_vigente())
    
    def test_get_presupuesto_display(self):
        """Test display del presupuesto"""
        # Presupuesto con rango
        oferta1 = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-rango',
            titulo='Oferta con rango',
            descripcion='Descripción',
            tipo_contrato='evento_unico',
            presupuesto_minimo=100000,
            presupuesto_maximo=200000,
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel
        )
        self.assertEqual(oferta1.get_presupuesto_display(), "$100,000 - $200,000 CLP")
        
        # Presupuesto a convenir
        oferta2 = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-convenir',
            titulo='Oferta a convenir',
            descripcion='Descripción',
            tipo_contrato='evento_unico',
            presupuesto_a_convenir=True,
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel
        )
        self.assertEqual(oferta2.get_presupuesto_display(), "A convenir")
    
    def test_cupos_restantes(self):
        """Test cálculo de cupos restantes"""
        oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-cupos',
            titulo='Oferta con cupos',
            descripcion='Descripción',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            cupos_disponibles=3
        )
        
        # Sin postulaciones aceptadas
        self.assertEqual(oferta.get_cupos_restantes(), 3)
    
    def test_auto_publicacion_fecha(self):
        """Test que la fecha de publicación se establece automáticamente"""
        oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-auto-fecha',
            titulo='Oferta auto fecha',
            descripcion='Descripción',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            estado='borrador'
        )
        
        self.assertIsNone(oferta.fecha_publicacion)
        
        # Cambiar a publicada
        oferta.estado = 'publicada'
        oferta.save()
        
        self.assertIsNotNone(oferta.fecha_publicacion)


class OfertaInstrumentoTest(TestCase):
    """Tests para relaciones OfertaInstrumento"""
    
    def setUp(self):
        # Crear datos básicos igual que antes
        self.instrumento1, _ = Instrumento.objects.get_or_create(
            nombre='Guitarra Test Rel',
            defaults={'categoria': 'Cuerda'}
        )
        self.instrumento2, _ = Instrumento.objects.get_or_create(
            nombre='Bajo Test Rel',
            defaults={'categoria': 'Cuerda'}
        )
        
        orden_unico = random.randint(3000, 9999)
        self.nivel, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Intermedio Test Rel {orden_unico}',
            defaults={'orden': orden_unico}
        )
        self.ubicacion, _ = Ubicacion.objects.get_or_create(
            nombre='Santiago Test Rel',
            defaults={'region': 'Región Metropolitana'}
        )
        
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_rel_test',
            email='empleador_rel@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Test Company Rel',
            ubicacion=self.ubicacion.nombre
        )
        
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-instrumentos-test',
            titulo='Oferta con instrumentos',
            descripcion='Descripción',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel
        )
    
    def test_agregar_instrumentos_requeridos(self):
        """Test agregar instrumentos requeridos a oferta"""
        # Agregar guitarrista como prioridad 1
        rel1 = OfertaInstrumento.objects.create(
            oferta_laboral=self.oferta,
            instrumento=self.instrumento1,
            prioridad=1,
            es_obligatorio=True
        )
        
        # Agregar bajista como prioridad 2
        rel2 = OfertaInstrumento.objects.create(
            oferta_laboral=self.oferta,
            instrumento=self.instrumento2,
            prioridad=2,
            es_obligatorio=False
        )
        
        instrumentos = self.oferta.get_instrumentos_requeridos()
        self.assertEqual(instrumentos.count(), 2)
        self.assertEqual(instrumentos.first().instrumento, self.instrumento1)
        self.assertTrue(instrumentos.first().es_obligatorio)


class OfertaLaboralViewsTest(TestCase):
    """Tests para las vistas de ofertas laborales"""
    
    def setUp(self):
        self.client = Client()
        
        # Crear datos de prueba
        orden_unico = random.randint(4000, 9999)
        self.nivel, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Intermedio Test Views {orden_unico}',
            defaults={'orden': orden_unico}
        )
        self.ubicacion, _ = Ubicacion.objects.get_or_create(
            nombre='Santiago Test Views',
            defaults={'region': 'Región Metropolitana'}
        )
        
        # Usuario empleador
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_views_test',
            email='empleador_views@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Test Company Views',
            ubicacion=self.ubicacion.nombre
        )
        
        # Usuario músico
        self.musico_user = Usuario.objects.create_user(
            username='musico_views_test',
            email='musico_views@test.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        
        # Oferta de prueba
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-views-test',
            titulo='Oferta Views Test',
            descripcion='Descripción para views test',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            estado='publicada'
        )
    
    def test_lista_ofertas_publicas_accesible(self):
        """Test que la lista de ofertas públicas es accesible"""
        response = self.client.get('/ofertas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)
    
    def test_detalle_oferta_accesible(self):
        """Test que el detalle de oferta es accesible con autenticación"""
        # El detalle requiere autenticación
        self.client.login(username='musico_views_test', password='testpass123')
        response = self.client.get(f'/ofertas/{self.oferta.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)
        self.assertContains(response, self.oferta.descripcion)
    
    def test_crear_oferta_requiere_autenticacion_empleador(self):
        """Test que crear oferta requiere estar autenticado como empleador"""
        # Sin autenticación
        response = self.client.get('/ofertas/nueva/')
        self.assertEqual(response.status_code, 302)  # Redirect a login
        
        # Con autenticación como músico
        self.client.login(username='musico_views_test', password='testpass123')
        response = self.client.get('/ofertas/nueva/')
        self.assertEqual(response.status_code, 302)  # Redirect por no ser empleador
        
        # Con autenticación como empleador
        self.client.login(username='empleador_views_test', password='testpass123')
        response = self.client.get('/ofertas/nueva/')
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_empleador_muestra_ofertas(self):
        """Test que el dashboard del empleador muestra sus ofertas"""
        self.client.login(username='empleador_views_test', password='testpass123')
        response = self.client.get('/ofertas/mis-ofertas/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta.titulo)


class BusquedaOfertasTest(TestCase):
    """Tests para la funcionalidad de búsqueda y filtrado de ofertas"""
    
    def setUp(self):
        # Crear datos de prueba para búsqueda
        self.ubicacion_stgo, _ = Ubicacion.objects.get_or_create(
            nombre='Santiago',
            defaults={'region': 'Región Metropolitana'}
        )
        self.ubicacion_valpo, _ = Ubicacion.objects.get_or_create(
            nombre='Valparaíso',
            defaults={'region': 'Región de Valparaíso'}
        )
        
        orden_unico_1 = random.randint(5000, 7000)
        orden_unico_2 = random.randint(7001, 9000)
        self.nivel_principiante, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Principiante Search {orden_unico_1}',
            defaults={'orden': orden_unico_1}
        )
        self.nivel_avanzado, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Avanzado Search {orden_unico_2}',
            defaults={'orden': orden_unico_2}
        )
        
        # Empleador
        empleador_user = Usuario.objects.create_user(
            username='empleador_search',
            email='empleador_search@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        empleador = PerfilEmpleador.objects.create(
            usuario=empleador_user,
            nombre_organizacion='Test Search Company',
            ubicacion=self.ubicacion_stgo.nombre
        )
        
        # Ofertas para testing
        self.oferta_rock = OfertaLaboral.objects.create(
            empleador=empleador,
            slug='guitarrista-rock',
            titulo='Guitarrista Rock Santiago',
            descripcion='Buscamos guitarrista para banda de rock',
            tipo_contrato='evento_unico',
            ubicacion=self.ubicacion_stgo,
            nivel_experiencia_minimo=self.nivel_principiante,
            estado='publicada',
            fecha_evento=timezone.now() + timedelta(days=20)
        )
        
        self.oferta_jazz = OfertaLaboral.objects.create(
            empleador=empleador,
            slug='pianista-jazz',
            titulo='Pianista Jazz Valparaíso',
            descripcion='Buscamos pianista para conjunto de jazz',
            tipo_contrato='contrato_temporal',
            ubicacion=self.ubicacion_valpo,
            nivel_experiencia_minimo=self.nivel_avanzado,
            estado='publicada',
            fecha_evento=timezone.now() + timedelta(days=30)
        )
        
        self.client = Client()
    
    def test_busqueda_por_titulo(self):
        """Test búsqueda por título"""
        response = self.client.get('/ofertas/', {
            'q': 'guitarrista'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta_rock.titulo)
        self.assertNotContains(response, self.oferta_jazz.titulo)
    
    def test_filtro_por_ubicacion(self):
        """Test filtro por ubicación"""
        response = self.client.get('/ofertas/', {
            'ubicacion': self.ubicacion_valpo.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta_jazz.titulo)
        self.assertNotContains(response, self.oferta_rock.titulo)
    
    def test_filtro_por_tipo_contrato(self):
        """Test filtro por nivel de experiencia"""
        response = self.client.get('/ofertas/', {
            'experiencia': self.nivel_principiante.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.oferta_rock.titulo)
        self.assertNotContains(response, self.oferta_jazz.titulo)
