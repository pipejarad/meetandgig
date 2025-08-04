"""
Tests para la funcionalidad de subida de foto de perfil
Ticket 2.3 - Subida de foto de perfil
"""

import tempfile
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

Usuario = get_user_model()


class FotoPerfilTestCase(TestCase):
    """Tests para la funcionalidad de foto de perfil"""
    
    def setUp(self):
        """Configuración inicial para los tests"""
        self.client = Client()
        self.usuario = Usuario.objects.create_user(
            username='testmusico',
            email='musico@test.com',
            password='testpass123',
            tipo_usuario='musico'
        )
    
    def crear_imagen_test(self, formato='JPEG', size=(200, 200)):
        """Crea una imagen de test en memoria"""
        image = Image.new('RGB', size, color='red')
        img_io = io.BytesIO()
        image.save(img_io, format=formato)
        img_io.seek(0)
        return img_io
    
    def test_modelo_usuario_tiene_campo_foto_perfil(self):
        """Verifica que el modelo Usuario tiene el campo foto_perfil"""
        self.assertTrue(hasattr(self.usuario, 'foto_perfil'))
        self.assertIsNone(self.usuario.foto_perfil.name)
    
    def test_subida_foto_perfil_valida(self):
        """Test de subida de foto de perfil válida"""
        self.client.login(username='testmusico', password='testpass123')
        
        # Crear imagen de test
        imagen_test = self.crear_imagen_test()
        uploaded_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=imagen_test.getvalue(),
            content_type='image/jpeg'
        )
        
        response = self.client.post(reverse('editar_perfil_musico'), {
            'biografia': 'Test biografia',
            'instrumento_principal': 'guitarra',
            'generos_musicales': 'rock',
            'nivel_experiencia': 'principiante',
            'años_experiencia': 1,
            'ubicacion': 'Santiago',
            'foto_perfil': uploaded_file
        })
        
        # Verificar que la foto se guardó
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.foto_perfil)
        self.assertIn('fotos_perfil/', self.usuario.foto_perfil.name)
    
    def test_validacion_imagen_muy_pequeña(self):
        """Test de validación para imagen demasiado pequeña"""
        from usuarios.forms import validate_image_file
        from django.core.exceptions import ValidationError
        
        # Crear imagen muy pequeña
        imagen_pequeña = self.crear_imagen_test(size=(50, 50))
        uploaded_file = SimpleUploadedFile(
            name='small_image.jpg',
            content=imagen_pequeña.getvalue(),
            content_type='image/jpeg'
        )
        
        with self.assertRaises(ValidationError):
            validate_image_file(uploaded_file)
    
    def test_validacion_archivo_muy_grande(self):
        """Test de validación para archivo demasiado grande"""
        from usuarios.forms import validate_image_file
        from django.core.exceptions import ValidationError
        
        # Simular archivo muy grande (mock del tamaño)
        imagen_test = self.crear_imagen_test()
        uploaded_file = SimpleUploadedFile(
            name='large_image.jpg',
            content=imagen_test.getvalue(),
            content_type='image/jpeg'
        )
        # Simular tamaño muy grande
        uploaded_file.size = 6 * 1024 * 1024  # 6MB
        
        with self.assertRaises(ValidationError):
            validate_image_file(uploaded_file)
    
    def test_validacion_formato_invalido(self):
        """Test de validación para formato de archivo inválido"""
        from usuarios.forms import validate_image_file
        from django.core.exceptions import ValidationError
        
        # Crear archivo que no sea imagen
        uploaded_file = SimpleUploadedFile(
            name='document.txt',
            content=b'Este es un archivo de texto',
            content_type='text/plain'
        )
        
        with self.assertRaises(ValidationError):
            validate_image_file(uploaded_file)
    
    def test_visualizacion_foto_perfil_en_template(self):
        """Test de que la foto de perfil se muestra en el template"""
        # Asignar una foto al usuario
        imagen_test = self.crear_imagen_test()
        uploaded_file = SimpleUploadedFile(
            name='profile.jpg',
            content=imagen_test.getvalue(),
            content_type='image/jpeg'
        )
        self.usuario.foto_perfil = uploaded_file
        self.usuario.save()
        
        self.client.login(username='testmusico', password='testpass123')
        
        # Crear perfil de músico primero
        from usuarios.models import PerfilMusico
        PerfilMusico.objects.create(
            usuario=self.usuario,
            biografia='Test',
            instrumento_principal='guitarra',
            generos_musicales='rock',
            ubicacion='Santiago'
        )
        
        response = self.client.get(reverse('ver_mi_perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.usuario.foto_perfil.url)
    
    def test_foto_perfil_opcional_en_registro(self):
        """Test de que la foto de perfil es opcional en el registro"""
        response = self.client.post(reverse('registro'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'tipo_usuario': 'musico'
            # Sin foto_perfil
        })
        
        # Debe redirigir exitosamente
        self.assertEqual(response.status_code, 302)
        
        # Verificar que el usuario se creó sin foto
        nuevo_usuario = Usuario.objects.get(username='newuser')
        self.assertFalse(nuevo_usuario.foto_perfil)


class FormularioFotoPerfilTestCase(TestCase):
    """Tests específicos para los formularios con foto de perfil"""
    
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            tipo_usuario='musico'
        )
    
    def test_formulario_registro_incluye_foto_perfil(self):
        """Verifica que el formulario de registro incluye el campo foto_perfil"""
        from usuarios.forms import RegistroForm
        form = RegistroForm()
        self.assertIn('foto_perfil', form.fields)
        self.assertFalse(form.fields['foto_perfil'].required)
    
    def test_formulario_perfil_musico_incluye_foto_perfil(self):
        """Verifica que el formulario de perfil músico incluye el campo foto_perfil"""
        from usuarios.forms import PerfilMusicoForm
        form = PerfilMusicoForm(usuario=self.usuario)
        self.assertIn('foto_perfil', form.fields)
        self.assertFalse(form.fields['foto_perfil'].required)
    
    def test_formulario_perfil_empleador_incluye_foto_perfil(self):
        """Verifica que el formulario de perfil empleador incluye el campo foto_perfil"""
        from usuarios.forms import PerfilEmpleadorForm
        form = PerfilEmpleadorForm(user=self.usuario)
        self.assertIn('foto_perfil', form.fields)
        self.assertFalse(form.fields['foto_perfil'].required)
