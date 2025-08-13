from django.test import TestCase, TransactionTestCase
from django.core.management import call_command
from django.db import connection
from usuarios.models import NivelExperiencia, Ubicacion


class CatalogosBasicTest(TestCase):
    """Tests básicos para modelos gestionados"""
    
    def test_nivel_experiencia_str(self):
        """Test que el método __str__ de NivelExperiencia funciona"""
        nivel = NivelExperiencia.objects.create(
            nombre='Profesional',
            orden=4,
            años_minimos=10
        )
        self.assertEqual(str(nivel), 'Profesional')
    
    def test_ubicacion_str(self):
        """Test que el método __str__ de Ubicacion funciona"""
        ubicacion = Ubicacion.objects.create(
            nombre='Santiago',
            region='Región Metropolitana'
        )
        self.assertEqual(str(ubicacion), 'Santiago, Región Metropolitana')


class ComandoPoblarTest(TestCase):
    """Test básico del comando poblar_catalogos"""
    
    def test_comando_help(self):
        """Test que el comando tiene help"""
        # Si el comando está bien configurado, esto no debería fallar
        from django.core.management import get_commands
        commands = get_commands()
        self.assertIn('poblar_catalogos', commands)
