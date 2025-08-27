"""
Tests para el sistema de notificaciones de Sprint 3
"""
import random
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from usuarios.models import (
    Usuario, PerfilMusico, PerfilEmpleador, Portafolio,
    OfertaLaboral, Postulacion, Notificacion,
    NivelExperiencia, Ubicacion
)


class NotificacionModelTest(TestCase):
    """Tests para el modelo Notificacion"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear catálogos únicos
        orden_unico = random.randint(40000, 49999)
        self.nivel, _ = NivelExperiencia.objects.get_or_create(
            nombre=f'Avanzado Test Notif {orden_unico}',
            defaults={'orden': orden_unico}
        )
        self.ubicacion, _ = Ubicacion.objects.get_or_create(
            nombre='Valparaíso Test Notif',
            defaults={'region': 'Región de Valparaíso'}
        )
        
        # Usuario empleador
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_notif_test',
            email='empleador_notif@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Empresa Notif Test',
            ubicacion=self.ubicacion.nombre
        )
        
        # Usuario músico
        self.musico_user = Usuario.objects.create_user(
            username='musico_notif_test',
            email='musico_notif@test.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        self.musico = PerfilMusico.objects.create(
            usuario=self.musico_user,
            telefono='+56977777777',
            direccion='Address Notif'
        )
        self.portafolio = Portafolio.objects.create(
            usuario=self.musico_user,
            slug='portafolio-notif-test',
            biografia='Pianista para tests de notificaciones',
            nivel_experiencia=self.nivel,
            ubicacion=self.ubicacion
        )
        
        # Oferta laboral
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            slug='oferta-notif-test',
            titulo='Pianista para eventos',
            descripcion='Oferta para test de notificaciones',
            tipo_contrato='freelance',
            fecha_evento=timezone.now() + timedelta(days=15),
            duracion_estimada='4 horas',
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel,
            presupuesto_minimo=200000,
            presupuesto_maximo=300000,
            estado='publicada'
        )
        
        # Postulación
        self.postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            portafolio=self.portafolio,
            tipo_postulacion='espontanea',
            mensaje_personalizado='Me interesa esta oportunidad'
        )
    
    def test_crear_notificacion_basica(self):
        """Test crear notificación básica"""
        notificacion = Notificacion.objects.create(
            empleador=self.empleador,
            tipo='postulacion_cancelada',
            titulo='Postulación cancelada',
            mensaje='El músico Juan Pérez canceló su postulación',
            postulacion=self.postulacion
        )
        
        self.assertEqual(notificacion.empleador, self.empleador)
        self.assertEqual(notificacion.tipo, 'postulacion_cancelada')
        self.assertEqual(notificacion.titulo, 'Postulación cancelada')
        self.assertEqual(notificacion.postulacion, self.postulacion)
        self.assertFalse(notificacion.leida)
        self.assertIsNone(notificacion.fecha_lectura)
        self.assertIsNotNone(notificacion.fecha_creacion)
    
    def test_marcar_como_leida(self):
        """Test marcar notificación como leída"""
        notificacion = Notificacion.objects.create(
            empleador=self.empleador,
            tipo='oferta_completada',
            titulo='Oferta completada',
            mensaje='Tu oferta ha sido completada exitosamente',
            oferta_laboral=self.oferta
        )
        
        # Inicialmente no leída
        self.assertFalse(notificacion.leida)
        self.assertIsNone(notificacion.fecha_lectura)
        
        # Marcar como leída
        notificacion.marcar_como_leida()
        
        # Verificar cambios
        self.assertTrue(notificacion.leida)
        self.assertIsNotNone(notificacion.fecha_lectura)
    
    def test_str_representation(self):
        """Test representación string de la notificación"""
        notificacion = Notificacion.objects.create(
            empleador=self.empleador,
            tipo='postulacion_cancelada',
            titulo='Test Notificación',
            mensaje='Mensaje de prueba'
        )
        
        expected = f"{self.empleador.nombre_organizacion} - Test Notificación"
        self.assertEqual(str(notificacion), expected)