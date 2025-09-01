"""
Tests para el sistema de notificaciones - Sprint 4 Tickets 4.4 y 4.5
Verificación de envío de emails y creación de notificaciones
"""

import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch

from usuarios.models import (
    Usuario, PerfilMusico, PerfilEmpleador, Portafolio, OfertaLaboral, 
    Postulacion, Notificacion, Ubicacion, NivelExperiencia
)
from usuarios.views import enviar_notificacion_nueva_postulacion, enviar_notificacion_resultado_postulacion


class NotificacionesTestCase(TestCase):
    """Tests para el sistema de notificaciones de postulaciones"""
    
    def setUp(self):
        """Configuración inicial para tests"""
        # Crear ubicación y nivel de experiencia
        self.ubicacion = Ubicacion.objects.create(
            nombre="Santiago Centro",
            region="Metropolitana",
            pais="Chile"
        )
        
        self.nivel_experiencia = NivelExperiencia.objects.create(
            nombre="Test Intermedio",
            años_minimos=2,
            años_maximos=5,
            orden=10  # Usar un orden único para tests
        )
        
        # Crear músico
        self.musico = Usuario.objects.create_user(
            username='musico_test',
            email='musico@test.com',
            password='testpass123',
            first_name='Juan',
            last_name='Músico',
            tipo_usuario='musico'
        )
        
        self.perfil_musico = PerfilMusico.objects.create(
            usuario=self.musico,
            telefono='+56912345678'
        )
        
        self.portafolio = Portafolio.objects.create(
            usuario=self.musico,
            biografia='Músico profesional',
            nivel_experiencia=self.nivel_experiencia,
            ubicacion=self.ubicacion,
            años_experiencia=3
        )
        
        # Crear empleador
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_test',
            email='empleador@test.com',
            password='testpass123',
            first_name='María',
            last_name='Empleadora',
            tipo_usuario='empleador'
        )
        
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Empresa Test',
            telefono='+56987654321'
        )
        
        # Crear oferta laboral
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            titulo='Guitarrista para evento',
            descripcion='Necesitamos guitarrista',
            fecha_evento=timezone.now() + timedelta(days=30),
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel_experiencia,  # Agregar campo requerido
            presupuesto_minimo=100000,
            presupuesto_maximo=200000,
            cupos_disponibles=1
        )
        
        # Cliente para requests
        self.client = Client()
    
    def test_envio_notificacion_nueva_postulacion(self):
        """Test: Verificar envío de email al empleador cuando recibe nueva postulación"""
        # Crear postulación
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico,
            portafolio=self.portafolio,  # Agregar portafolio requerido
            mensaje_personalizado='Hola, me interesa participar'
        )
        
        # Limpiar emails anteriores
        mail.outbox = []
        
        # Enviar notificación
        resultado = enviar_notificacion_nueva_postulacion(postulacion)
        
        # Verificar que se envió correctamente
        self.assertTrue(resultado)
        
        # Verificar que se envió un email
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertIn(self.empleador_user.email, email.to)
        self.assertIn('Nueva postulación', email.subject)
        self.assertIn(self.musico.get_full_name(), email.body)
        self.assertIn(self.oferta.titulo, email.body)
        
        # Verificar que se creó notificación en BD
        notificacion = Notificacion.objects.filter(
            empleador=self.empleador,
            tipo='nueva_postulacion',
            postulacion=postulacion
        ).first()
        
        self.assertIsNotNone(notificacion)
        self.assertIn(self.oferta.titulo, notificacion.titulo)
        self.assertFalse(notificacion.leida)
    
    def test_envio_notificacion_postulacion_aceptada(self):
        """Test: Verificar envío de email al músico cuando postulación es aceptada"""
        # Crear postulación
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico,
            portafolio=self.portafolio,  # Agregar portafolio requerido
            estado='pendiente'
        )
        
        # Limpiar emails anteriores
        mail.outbox = []
        
        # Enviar notificación de aceptación
        resultado = enviar_notificacion_resultado_postulacion(
            postulacion=postulacion,
            aceptada=True
        )
        
        # Verificar que se envió correctamente
        self.assertTrue(resultado)
        
        # Verificar que se envió un email
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertIn(self.musico.email, email.to)
        self.assertIn('Postulación aceptada', email.subject)
        self.assertIn('FELICIDADES', email.body)
        self.assertIn(self.oferta.titulo, email.body)
    
    def test_envio_notificacion_postulacion_rechazada(self):
        """Test: Verificar envío de email al músico cuando postulación es rechazada"""
        # Crear postulación
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico,
            portafolio=self.portafolio,  # Agregar portafolio requerido
            estado='pendiente'
        )
        
        # Limpiar emails anteriores
        mail.outbox = []
        
        # Enviar notificación de rechazo
        resultado = enviar_notificacion_resultado_postulacion(
            postulacion=postulacion,
            aceptada=False
        )
        
        # Verificar que se envió correctamente
        self.assertTrue(resultado)
        
        # Verificar que se envió un email
        self.assertEqual(len(mail.outbox), 1)
        
        email = mail.outbox[0]
        self.assertIn(self.musico.email, email.to)
        self.assertIn('Resultado de postulación', email.subject)
        self.assertIn('No te desanimes', email.body)
        self.assertIn(self.oferta.titulo, email.body)
    
    def test_integracion_postulacion_completa(self):
        """Test: Verificar flujo completo de postulación con notificaciones"""
        # Login como músico
        self.client.login(username='musico_test', password='testpass123')
        
        # Limpiar emails
        mail.outbox = []
        
        # Hacer postulación
        response = self.client.post(
            reverse('postular_oferta', kwargs={'slug': self.oferta.slug}),
            {
                'mensaje_personalizado': 'Me interesa mucho esta oportunidad',
                'disponibilidad_fecha': True
            }
        )
        
        # Verificar que se redirigió correctamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se creó la postulación
        postulacion = Postulacion.objects.filter(
            oferta_laboral=self.oferta,
            musico=self.musico
        ).first()
        
        self.assertIsNotNone(postulacion)
        
        # Verificar que se envió email al empleador
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.empleador_user.email, mail.outbox[0].to)
        
        # Logout del músico y login como empleador
        self.client.logout()
        self.client.login(username='empleador_test', password='testpass123')
        
        # Limpiar emails para segunda parte
        mail.outbox = []
        
        # Procesar postulación (aceptar)
        response = self.client.post(
            reverse('procesar_postulacion', kwargs={
                'slug': self.oferta.slug,
                'postulacion_id': postulacion.id
            }),
            {
                'accion': 'aceptar',
                'notas': 'Perfil excelente, aceptado'
            }
        )
        
        # Verificar que se redirigió correctamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se actualizó el estado
        postulacion.refresh_from_db()
        self.assertEqual(postulacion.estado, 'aceptada')
        
        # Verificar que se envió email al músico
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.musico.email, mail.outbox[0].to)
        self.assertIn('aceptada', mail.outbox[0].subject.lower())
    
    @patch('usuarios.views.send_mail')
    def test_manejo_errores_email(self, mock_send_mail):
        """Test: Verificar manejo de errores al enviar emails"""
        # Configurar mock para que falle
        mock_send_mail.side_effect = Exception("Error de SMTP")
        
        # Crear postulación
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico,
            portafolio=self.portafolio  # Agregar portafolio requerido
        )
        
        # Intentar enviar notificación
        resultado = enviar_notificacion_nueva_postulacion(postulacion)
        
        # Verificar que se manejó el error
        self.assertFalse(resultado)
        
        # Verificar que se llamó send_mail
        mock_send_mail.assert_called_once()
    
    def test_contenido_templates_email(self):
        """Test: Verificar que los templates de email contienen la información correcta"""
        # Crear postulación con datos específicos
        postulacion = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico,
            portafolio=self.portafolio,  # Agregar portafolio requerido
            mensaje_personalizado='Mensaje de presentación personalizado'
        )
        
        # Limpiar emails
        mail.outbox = []
        
        # Enviar notificación
        enviar_notificacion_nueva_postulacion(postulacion)
        
        # Verificar contenido del email
        email = mail.outbox[0]
        
        # Verificar que contiene datos del músico
        self.assertIn(self.musico.get_full_name(), email.body)
        self.assertIn(self.musico.email, email.body)
        
        # Verificar que contiene datos de la oferta
        self.assertIn(self.oferta.titulo, email.body)
        self.assertIn(str(self.oferta.presupuesto_minimo), email.body)
        
        # Verificar que contiene el mensaje personalizado
        self.assertIn('Mensaje de presentación personalizado', email.body)
        
        # Verificar que tiene HTML y texto plano
        self.assertTrue(hasattr(email, 'alternatives'))


class AdminModerationTestCase(TestCase):
    """Tests para las mejoras de moderación en Django Admin"""
    
    def setUp(self):
        """Configuración para tests de admin"""
        # Crear superusuario
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Crear datos de test (similar al setUp anterior)
        self.ubicacion = Ubicacion.objects.create(
            nombre="Santiago Centro",
            region="Metropolitana"
        )
        
        self.nivel_experiencia = NivelExperiencia.objects.create(
            nombre="Test Admin",
            años_minimos=2,
            orden=11  # Usar un orden único para tests de admin
        )
        
        # Músico y empleador
        self.musico = Usuario.objects.create_user(
            username='musico_admin_test',
            email='musico_admin@test.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        
        PerfilMusico.objects.create(usuario=self.musico)
        
        self.portafolio = Portafolio.objects.create(
            usuario=self.musico,
            nivel_experiencia=self.nivel_experiencia,
            ubicacion=self.ubicacion
        )
        
        self.empleador_user = Usuario.objects.create_user(
            username='empleador_admin_test',
            email='empleador_admin@test.com',
            password='testpass123',
            tipo_usuario='empleador'
        )
        
        self.empleador = PerfilEmpleador.objects.create(
            usuario=self.empleador_user,
            nombre_organizacion='Empresa Admin Test'
        )
        
        self.oferta = OfertaLaboral.objects.create(
            empleador=self.empleador,
            titulo='Test Admin Oferta',
            ubicacion=self.ubicacion,
            nivel_experiencia_minimo=self.nivel_experiencia,  # Agregar campo requerido
            fecha_evento=timezone.now() + timedelta(days=30)
        )
        
        self.client = Client()
    
    def test_admin_login_access(self):
        """Test: Verificar acceso al admin con mejoras"""
        # Login como admin
        self.client.login(username='admin', password='adminpass123')
        
        # Acceder a la lista de postulaciones
        response = self.client.get('/admin/usuarios/postulacion/')
        self.assertEqual(response.status_code, 200)
        
        # Acceder a la lista de ofertas
        response = self.client.get('/admin/usuarios/ofertalaboral/')
        self.assertEqual(response.status_code, 200)
        
        # Acceder a la lista de notificaciones
        response = self.client.get('/admin/usuarios/notificacion/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_postulacion_actions(self):
        """Test: Verificar acciones en lote para postulaciones"""
        # Crear postulaciones
        postulacion1 = Postulacion.objects.create(
            oferta_laboral=self.oferta,
            musico=self.musico,
            portafolio=self.portafolio,  # Agregar portafolio requerido
            estado='pendiente'
        )
        
        # Login como admin
        self.client.login(username='admin', password='adminpass123')
        
        # Limpiar emails
        mail.outbox = []
        
        # Ejecutar acción de aceptar en lote
        response = self.client.post('/admin/usuarios/postulacion/', {
            'action': 'aceptar_postulaciones',
            '_selected_action': [postulacion1.id],
        })
        
        # Verificar redirección (acción ejecutada)
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se actualizó el estado
        postulacion1.refresh_from_db()
        self.assertEqual(postulacion1.estado, 'aceptada')
        
        # Verificar que se envió email
        self.assertEqual(len(mail.outbox), 1)


if __name__ == '__main__':
    # Ejecutar tests específicos
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    if not settings.configured:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')
        django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['usuarios.tests_sprint_4_notificaciones'])
    
    if failures:
        print(f"❌ {failures} tests fallaron")
    else:
        print("✅ Todos los tests pasaron exitosamente")
