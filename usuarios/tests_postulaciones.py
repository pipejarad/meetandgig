"""
Tests para el sistema de postulaciones de Sprint 3
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
    Usuario, PerfilMusico, PerfilEmpleador, Portafolio,
    OfertaLaboral, Postulacion, Notificacion,
    Instrumento, Genero, NivelExperiencia, Ubicacion
)

User = get_user_model()


class PostulacionModelTest(TestCase):
    """Tests para el modelo Postulacion"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear catálogos únicos
        self.instrumento, _ = Instrumento.objects.get_or_create(
            nombre='Guitarra Test Post',
            defaults={'categoria': 'Cuerda'}
        )
        self.genero, _ = Genero.objects.get_or_create(
            nombre='Rock Test Post',
            defaults={}
        )
        orden_unico = random.randint(10000, 19999)
        self.nivel, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Intermedio Test Post {orden_unico}',
            defaults={'orden': orden_unico}
        )
        self.ubicacion, _ = Ubicacion.objects.get_or_create(
            nombre='Santiago Test Post',
            defaults={'region': 'Región Metropolitana'}
        )
        
        # Usuario empleador
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_post_test',
            email='empleador_post@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Test Company Post',
            ubicacion=self.ubicacion.nombre
        )
        
        # Usuario músico
        self.musico_user = Usuario.objects.create_user(
            username='musico_post_test',
            email='musico_post@test.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        self.musico = PerfilMusico.objects.create(
            usuario=self.musico_user,
            telefono='+56987654321',
            direccion='Test Address Post'
        )
        self.portafolio = Portafolio.objects.create(
            usuario=self.musico_user,
            slug='portafolio-post-test',
            biografia='Biografía del músico test post',
            nivel_experiencia=self.nivel,
            ubicacion=self.ubicacion
        )
        
        # Oferta laboral
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-post-test',
            titulo='Guitarrista para postulación test',
            descripcion='Oferta para test de postulaciones',
            tipo_contrato='evento_unico',
            fecha_evento=timezone.now() + timedelta(days=30),
            duracion_estimada='3 horas',
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            presupuesto_minimo=100000,
            presupuesto_maximo=200000,
            estado='publicada'
        )
    
    def test_crear_postulacion_basica(self):
        """Test crear postulación básica"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            tipo_postulacion='espontanea',
            mensaje_personalizado='Me interesa participar en este proyecto'
        )
        
        self.assertEqual(postulacion.oferta_laboral, self.oferta)
        self.assertEqual(postulacion.musico, self.musico_user)
        self.assertEqual(postulacion.portafolio, self.portafolio)
        self.assertEqual(postulacion.estado, 'pendiente')  # Estado por defecto
        self.assertEqual(postulacion.tipo_postulacion, 'espontanea')
        self.assertIsNotNone(postulacion.fecha_postulacion)
    
    def test_unique_constraint_oferta_musico(self):
        """Test que no se pueden crear postulaciones duplicadas"""
        # Crear primera postulación
        Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            tipo_postulacion='espontanea'
        )
        
        # Intentar crear postulación duplicada
        with self.assertRaises(IntegrityError):
            Postulacion.objects.create(
                oferta_laboral=self.oferta,
                musico=self.musico_user,
                portafolio=self.portafolio,
                tipo_postulacion='espontanea'
            )
    
    def test_aceptar_postulacion(self):
        """Test aceptar postulación"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            tipo_postulacion='espontanea',
            mensaje_personalizado='Mensaje de prueba'
        )
        
        # Aceptar postulación
        postulacion.estado = 'aceptada'
        postulacion.save()
        
        self.assertEqual(postulacion.estado, 'aceptada')
        self.assertIsNotNone(postulacion.fecha_respuesta)
    
    def test_rechazar_postulacion(self):
        """Test rechazar postulación"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            tipo_postulacion='espontanea',
            mensaje_personalizado='Mensaje de prueba'
        )
        
        # Rechazar postulación
        postulacion.estado = 'rechazada'
        postulacion.notas_empleador = 'No se ajusta al perfil'
        postulacion.save()
        
        self.assertEqual(postulacion.estado, 'rechazada')
        self.assertEqual(postulacion.notas_empleador, 'No se ajusta al perfil')
        self.assertIsNotNone(postulacion.fecha_respuesta)
    
    def test_cancelar_postulacion_por_musico(self):
        """Test que músico puede cancelar su postulación"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            tipo_postulacion='espontanea'
        )
        
        # Músico cancela su postulación
        postulacion.estado = 'cancelada'
        postulacion.save()
        
        self.assertEqual(postulacion.estado, 'cancelada')
    
    def test_puede_ser_aceptada(self):
        """Test verificar si postulación puede ser aceptada"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            estado='pendiente'
        )
        
        self.assertTrue(postulacion.esta_pendiente())
        
        # Una vez aceptada, ya no está pendiente
        postulacion.estado = 'aceptada'
        postulacion.save()
        self.assertFalse(postulacion.esta_pendiente())
    
    def test_puede_ser_rechazada(self):
        """Test verificar si postulación puede ser rechazada"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            estado='en_revision'
        )
        
        self.assertTrue(postulacion.esta_pendiente())
        
        # Una vez rechazada, ya no está pendiente
        postulacion.estado = 'rechazada'
        postulacion.save()
        self.assertFalse(postulacion.esta_pendiente())
    
    def test_puede_ser_cancelada(self):
        """Test verificar si postulación puede ser cancelada por músico"""
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            estado='pendiente'
        )
        
        # El músico puede cancelar mientras esté pendiente
        self.assertTrue(postulacion.esta_pendiente())
        
        # Cancelar
        postulacion.estado = 'cancelada'
        postulacion.save()
        self.assertEqual(postulacion.estado, 'cancelada')