"""
Tests para el modelo Invitacion y funcionalidades de invitación directa
Ticket 3.8 - FASE 1: Modelo de Invitación
"""
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from usuarios.models import (
    PerfilEmpleador, PerfilMusico, Portafolio, OfertaLaboral, 
    Invitacion, Postulacion, Instrumento, Genero, NivelExperiencia, Ubicacion
)

User = get_user_model()


class InvitacionModelTest(TestCase):
    """Tests para el modelo Invitacion"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear catálogos básicos usando get_or_create para evitar duplicados
        self.instrumento, _ = Instrumento.objects.get_or_create(
            nombre='Guitarra Test',
            defaults={'categoria': 'Cuerda'}
        )
        self.genero, _ = Genero.objects.get_or_create(
            nombre='Rock Test',
            defaults={}
        )
        self.nivel, _ = NivelExperiencia.objects.get_or_create(
            nombre='Intermedio Test',
            defaults={'orden': 2}
        )
        self.ubicacion, _ = Ubicacion.objects.get_or_create(
            nombre='Santiago Centro Test',
            defaults={'tipo': 'comuna', 'region': 'Región Metropolitana'}
        )
        
        # Crear usuarios
        self.empleador_user = User.objects.create_user(
            username='empleador_test',
            email='empleador@test.com',
            password='password123',
            tipo_usuario='empleador'
        )
        
        self.musico_user = User.objects.create_user(
            username='musico_test',
            email='musico@test.com',
            password='password123',
            tipo_usuario='musico'
        )
        
        # Crear perfiles
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_empresa='Test Company',
            rut_empresa='12345678-9',
            telefono='+56912345678',
            ubicacion=self.ubicacion
        )
        
        self.musico = PerfilMusico.objects.create(
            usuario=self.musico_user,
            telefono='+56987654321',
            fecha_nacimiento='1990-01-01',
            direccion='Test Address'
        )
        
        # Crear portafolio
        self.portafolio = Portafolio.objects.create(
            musico=self.musico,
            titulo='Portafolio Test',
            descripcion='Descripción del portafolio',
            nivel_experiencia=self.nivel,
            ubicacion=self.ubicacion
        )
        
        # Crear oferta laboral
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            titulo='Guitarrista para concierto',
            descripcion='Buscamos guitarrista experimentado',
            tipo_contrato='evento_unico',
            salario_minimo=100000,
            salario_maximo=200000,
            fecha_evento='2024-12-31',
            ubicacion=self.ubicacion,
            numero_musicos_requeridos=1,
            estado='publicada'
        )
    
    def test_crear_invitacion(self):
        """Test crear invitación básica"""
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Te invitamos a participar en nuestro evento',
            tarifa_ofrecida=150000
        )
        
        self.assertEqual(invitacion.estado, 'pendiente')
        self.assertTrue(invitacion.esta_pendiente())
        self.assertFalse(invitacion.ha_expirado())
        self.assertTrue(invitacion.puede_ser_aceptada())
        self.assertTrue(invitacion.puede_ser_rechazada())
        self.assertTrue(invitacion.puede_ser_cancelada())
    
    def test_fecha_expiracion_automatica(self):
        """Test que la fecha de expiración se configura automáticamente"""
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Test mensaje'
        )
        
        # Debe configurarse automáticamente a 7 días
        esperado = invitacion.fecha_invitacion + timezone.timedelta(days=7)
        self.assertEqual(invitacion.fecha_expiracion.date(), esperado.date())
    
    def test_aceptar_invitacion(self):
        """Test aceptar invitación crea postulación automáticamente"""
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Test mensaje',
            tarifa_ofrecida=150000
        )
        
        # Aceptar invitación
        postulacion = invitacion.aceptar(
            mensaje_respuesta='Acepto la invitación',
            tarifa_propuesta=160000
        )
        
        # Verificar estado de invitación
        invitacion.refresh_from_db()
        self.assertEqual(invitacion.estado, 'aceptada')
        self.assertEqual(invitacion.mensaje_respuesta, 'Acepto la invitación')
        self.assertIsNotNone(invitacion.fecha_respuesta)
        self.assertEqual(invitacion.postulacion_creada, postulacion)
        
        # Verificar postulación creada
        self.assertEqual(postulacion.tipo_postulacion, 'invitacion')
        self.assertEqual(postulacion.estado, 'pendiente')
        self.assertEqual(postulacion.tarifa_propuesta, 160000)
        self.assertEqual(postulacion.mensaje_personalizado, 'Acepto la invitación')
    
    def test_rechazar_invitacion(self):
        """Test rechazar invitación"""
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Test mensaje'
        )
        
        # Rechazar invitación
        invitacion.rechazar('No puedo en esa fecha')
        
        # Verificar estado
        invitacion.refresh_from_db()
        self.assertEqual(invitacion.estado, 'rechazada')
        self.assertEqual(invitacion.mensaje_respuesta, 'No puedo en esa fecha')
        self.assertIsNotNone(invitacion.fecha_respuesta)
        self.assertIsNone(invitacion.postulacion_creada)
    
    def test_cancelar_invitacion(self):
        """Test cancelar invitación por empleador"""
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Test mensaje'
        )
        
        # Cancelar invitación
        invitacion.cancelar()
        
        # Verificar estado
        invitacion.refresh_from_db()
        self.assertEqual(invitacion.estado, 'cancelada')
    
    def test_invitacion_expirada(self):
        """Test marcar invitación como expirada"""
        # Crear invitación con fecha pasada
        fecha_pasada = timezone.now() - timezone.timedelta(days=1)
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Test mensaje',
            fecha_expiracion=fecha_pasada
        )
        
        # Verificar que ha expirado
        self.assertTrue(invitacion.ha_expirado())
        self.assertFalse(invitacion.puede_ser_aceptada())
        
        # Marcar como expirada
        invitacion.marcar_como_expirada()
        
        # Verificar estado
        invitacion.refresh_from_db()
        self.assertEqual(invitacion.estado, 'expirada')
    
    def test_unique_together_constraint(self):
        """Test que no se pueden crear invitaciones duplicadas"""
        # Crear primera invitación
        Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Primera invitación'
        )
        
        # Intentar crear segunda invitación (debe fallar)
        with self.assertRaises(Exception):
            Invitacion.objects.create(
                oferta_laboral=self.oferta,
                musico=self.musico_user,
                empleador=self.empleador,
                portafolio=self.portafolio,
                mensaje_invitacion='Segunda invitación'
            )
    
    def test_dias_restantes(self):
        """Test cálculo de días restantes"""
        # Invitación con 3 días restantes
        fecha_futura = timezone.now() + timezone.timedelta(days=3)
        invitacion = Invitacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico_user,
            empleador=self.empleador,
            portafolio=self.portafolio,
            mensaje_invitacion='Test mensaje',
            fecha_expiracion=fecha_futura
        )
        
        # Debe retornar aproximadamente 3 días
        dias = invitacion.dias_restantes()
        self.assertGreaterEqual(dias, 2)  # Al menos 2 días
        self.assertLessEqual(dias, 3)     # Máximo 3 días
