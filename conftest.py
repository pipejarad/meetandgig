"""
Configuración de fixtures y configuraciones globales para pytest
"""
import os
import sys
import django
from pathlib import Path

# Configurar Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')

# Agregar el directorio del proyecto al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configurar Django
django.setup()

import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from django.core.management import call_command
from usuarios.models import (
    PerfilMusico, PerfilEmpleador, Portafolio, OfertaLaboral,
    Instrumento, Genero, NivelExperiencia, Ubicacion
)

Usuario = get_user_model()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """
    Configuración de base de datos para la sesión de testing.
    Carga datos de catálogos necesarios una sola vez.
    """
    with django_db_blocker.unblock():
        # Cargar datos de catálogos si existen comandos para ello
        try:
            call_command('loaddata', 'catalogos_iniciales.json', verbosity=0)
        except:
            # Si no existe el fixture, crear datos mínimos
            pass


@pytest.fixture
def client():
    """Cliente de testing de Django"""
    return Client()


@pytest.fixture
def usuario_musico():
    """Usuario tipo músico para testing"""
    return Usuario.objects.create_user(
        username='musico_test',
        email='musico@test.com',
        password='testpass123',
        tipo_usuario='musico'
    )


@pytest.fixture
def usuario_empleador():
    """Usuario tipo empleador para testing"""
    return Usuario.objects.create_user(
        username='empleador_test',
        email='empleador@test.com',
        password='testpass123',
        tipo_usuario='empleador'
    )


@pytest.fixture
def perfil_musico(usuario_musico):
    """Perfil de músico completo para testing"""
    return PerfilMusico.objects.create(
        usuario=usuario_musico,
        nombre='Juan',
        apellido='Pérez',
        telefono='+56912345678',
        fecha_nacimiento='1990-01-01',
        ubicacion='Santiago, Chile',
        biografia='Músico profesional con 10 años de experiencia.',
        disponibilidad_horaria='tarde',
        tarifa_hora=50000,
        perfil_publico=True
    )


@pytest.fixture
def perfil_empleador(usuario_empleador):
    """Perfil de empleador para testing"""
    return PerfilEmpleador.objects.create(
        usuario=usuario_empleador,
        nombre_organizacion='Empresa Test',
        tipo_entidad='empresa',
        ubicacion='Santiago, Chile',
        descripcion='Empresa dedicada a eventos musicales.',
        telefono_contacto='+56987654321'
    )


@pytest.fixture
def ubicacion():
    """Ubicación para testing"""
    ubicacion, _ = Ubicacion.objects.get_or_create(
        nombre='Santiago',
        defaults={
            'region': 'Región Metropolitana',
            'pais': 'Chile'
        }
    )
    return ubicacion


@pytest.fixture
def nivel_experiencia():
    """Nivel de experiencia para testing"""
    nivel, _ = NivelExperiencia.objects.get_or_create(
        nombre='Intermedio',
        defaults={
            'descripcion': '2-5 años de experiencia',
            'orden': 2,
            'años_minimos': 2,
            'años_maximos': 5
        }
    )
    return nivel


@pytest.fixture
def instrumento_guitarra():
    """Instrumento guitarra para testing"""
    instrumento, _ = Instrumento.objects.get_or_create(
        nombre='Guitarra',
        defaults={'categoria': 'Cuerdas'}
    )
    return instrumento


@pytest.fixture
def genero_rock():
    """Género rock para testing"""
    genero, _ = Genero.objects.get_or_create(
        nombre='Rock',
        defaults={'descripcion': 'Género musical rock'}
    )
    return genero


@pytest.fixture
def portafolio_completo(perfil_musico, ubicacion, nivel_experiencia):
    """Portafolio completo para testing"""
    return Portafolio.objects.create(
        usuario=perfil_musico.usuario,
        titulo='Guitarrista Profesional',
        descripcion_servicios='Servicios musicales profesionales',
        experiencia_años=5,
        ubicacion=ubicacion,
        nivel_experiencia=nivel_experiencia,
        tarifa_base=100000,
        disponible_para_gigs=True,
        activo=True
    )


@pytest.fixture
def oferta_laboral(perfil_empleador, ubicacion, nivel_experiencia):
    """Oferta laboral para testing"""
    return OfertaLaboral.objects.create(
        empleador=perfil_empleador,
        titulo='Guitarrista para evento',
        descripcion='Buscamos guitarrista para evento corporativo',
        tipo_contrato='evento_unico',
        ubicacion=ubicacion,
        nivel_experiencia_minimo=nivel_experiencia,
        presupuesto_minimo=100000,
        presupuesto_maximo=200000,
        cupos_disponibles=1,
        estado='publicada'
    )


@pytest.fixture
def authenticated_client_musico(client, usuario_musico):
    """Cliente autenticado como músico"""
    client.login(username='musico@test.com', password='testpass123')
    return client


@pytest.fixture
def authenticated_client_empleador(client, usuario_empleador):
    """Cliente autenticado como empleador"""
    client.login(username='empleador@test.com', password='testpass123')
    return client


class TestDataMixin:
    """
    Mixin con métodos helper para crear datos de testing
    """
    
    @staticmethod
    def create_usuario(tipo_usuario='musico', **kwargs):
        """Helper para crear usuarios"""
        defaults = {
            'username': f'{tipo_usuario}_test',
            'email': f'{tipo_usuario}@test.com',
            'password': 'testpass123',
            'tipo_usuario': tipo_usuario
        }
        defaults.update(kwargs)
        return Usuario.objects.create_user(**defaults)
    
    @staticmethod
    def create_multiple_usuarios(count=5, tipo_usuario='musico'):
        """Helper para crear múltiples usuarios"""
        usuarios = []
        for i in range(count):
            usuario = TestDataMixin.create_usuario(
                tipo_usuario=tipo_usuario,
                username=f'{tipo_usuario}_test_{i}',
                email=f'{tipo_usuario}{i}@test.com'
            )
            usuarios.append(usuario)
        return usuarios
