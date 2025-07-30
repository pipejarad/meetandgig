from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from .forms import RegistroForm
from .models import Usuario

User = get_user_model()


class UsuarioModelTest(TestCase):
    """Tests para el modelo Usuario"""
    
    def test_create_user_with_email(self):
        """Test crear usuario con email único"""
        user = User.objects.create_user(
            username='testuser',
            email='test@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        self.assertEqual(user.email, 'test@ejemplo.com')
        self.assertEqual(user.tipo_usuario, 'musico')
        self.assertTrue(user.check_password('testpass123'))

    def test_email_unique_constraint(self):
        """Test que el email debe ser único"""
        User.objects.create_user(
            username='user1',
            email='test@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='user2',
                email='test@ejemplo.com',
                password='testpass123',
                tipo_usuario='empleador'
            )


class RegistroFormTest(TestCase):
    """Tests para el formulario de registro"""
    
    def test_valid_form(self):
        """Test formulario válido"""
        form_data = {
            'username': 'testuser',
            'email': 'test@ejemplo.com',
            'tipo_usuario': 'musico',
            'password1': 'testpass123ABC',
            'password2': 'testpass123ABC',
        }
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_duplicate_email(self):
        """Test email duplicado"""
        User.objects.create_user(
            username='existing',
            email='test@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        
        form_data = {
            'username': 'newuser',
            'email': 'test@ejemplo.com',
            'tipo_usuario': 'empleador',
            'password1': 'testpass123ABC',
            'password2': 'testpass123ABC',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este email ya está registrado.', form.errors['email'])

    def test_duplicate_username(self):
        """Test username duplicado"""
        User.objects.create_user(
            username='testuser',
            email='test1@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        
        form_data = {
            'username': 'testuser',
            'email': 'test2@ejemplo.com',
            'tipo_usuario': 'empleador',
            'password1': 'testpass123ABC',
            'password2': 'testpass123ABC',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Este nombre de usuario ya está en uso.', form.errors['username'])


class RegistroViewTest(TestCase):
    """Tests para la vista de registro"""
    
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('registro')

    def test_get_register_page(self):
        """Test GET a la página de registro"""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Registro de usuario')

    def test_successful_registration(self):
        """Test registro exitoso"""
        form_data = {
            'username': 'newuser',
            'email': 'new@ejemplo.com',
            'tipo_usuario': 'musico',
            'password1': 'testpass123ABC',
            'password2': 'testpass123ABC',
        }
        response = self.client.post(self.register_url, data=form_data, follow=True)
        
        # Verificar que el usuario fue creado
        self.assertTrue(User.objects.filter(email='new@ejemplo.com').exists())
        
        # Debe redirigir después del registro exitoso
        self.assertEqual(response.status_code, 200)  # 200 porque seguimos la redirección
        
        # Verificar que llegamos a la página correcta
        self.assertContains(response, 'Meet & Gig')  # O cualquier contenido de la página inicio

    def test_registration_with_existing_email(self):
        """Test registro con email existente"""
        # Crear usuario existente
        User.objects.create_user(
            username='existing',
            email='existing@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        
        form_data = {
            'username': 'newuser',
            'email': 'existing@ejemplo.com',
            'tipo_usuario': 'empleador',
            'password1': 'testpass123ABC',
            'password2': 'testpass123ABC',
        }
        response = self.client.post(self.register_url, data=form_data)
        
        # Debe mantenerse en la página de registro
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este email ya está registrado.')

    def test_authenticated_user_redirect(self):
        """Test que usuario autenticado sea redirigido"""
        user = User.objects.create_user(
            username='testuser',
            email='test@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        self.client.login(username='test@ejemplo.com', password='testpass123')
        
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 302)


class AuthenticationTest(TestCase):
    """Tests para autenticación con email"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@ejemplo.com',
            password='testpass123',
            tipo_usuario='musico'
        )
        self.client = Client()
        self.login_url = reverse('login')

    def test_login_with_email(self):
        """Test login con email"""
        response = self.client.post(self.login_url, {
            'username': 'test@ejemplo.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_username(self):
        """Test login con username"""
        response = self.client.post(self.login_url, {
            'username': 'testuser', 
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
