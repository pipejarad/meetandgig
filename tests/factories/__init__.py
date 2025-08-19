"""
Factories para crear objetos de testing usando Factory Boy
"""
import factory
from factory import django, fuzzy
from django.contrib.auth import get_user_model
from faker import Faker
from usuarios.models import (
    PerfilMusico, PerfilEmpleador, Portafolio, OfertaLaboral,
    Instrumento, Genero, NivelExperiencia, Ubicacion,
    PortafolioInstrumento, PortafolioGenero, Multimedia
)

fake = Faker('es_ES')
Usuario = get_user_model()


class UsuarioFactory(django.DjangoModelFactory):
    """Factory para crear usuarios"""
    
    class Meta:
        model = Usuario
    
    username = factory.Sequence(lambda n: f"usuario_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    first_name = factory.LazyFunction(fake.first_name)
    last_name = factory.LazyFunction(fake.last_name)
    tipo_usuario = fuzzy.FuzzyChoice(['musico', 'empleador'])
    is_active = True


class MusicoFactory(UsuarioFactory):
    """Factory específico para músicos"""
    tipo_usuario = 'musico'


class EmpleadorFactory(UsuarioFactory):
    """Factory específico para empleadores"""
    tipo_usuario = 'empleador'


class UbicacionFactory(django.DjangoModelFactory):
    """Factory para ubicaciones"""
    
    class Meta:
        model = Ubicacion
        django_get_or_create = ('nombre',)
    
    nombre = fuzzy.FuzzyChoice([
        'Santiago', 'Valparaíso', 'Concepción', 'La Serena', 
        'Antofagasta', 'Temuco', 'Iquique', 'Valdivia'
    ])
    region = factory.LazyAttribute(
        lambda obj: "Región Metropolitana" if obj.nombre == 'Santiago' 
        else f"Región de {obj.nombre}"
    )
    pais = 'Chile'


class InstrumentoFactory(django.DjangoModelFactory):
    """Factory para instrumentos"""
    
    class Meta:
        model = Instrumento
        django_get_or_create = ('nombre',)
    
    nombre = fuzzy.FuzzyChoice([
        'Guitarra', 'Piano', 'Batería', 'Bajo', 'Violín', 
        'Saxofón', 'Trompeta', 'Flauta', 'Guitarra Eléctrica'
    ])
    categoria = factory.LazyAttribute(
        lambda obj: {
            'Guitarra': 'Cuerdas',
            'Piano': 'Teclas',
            'Batería': 'Percusión',
            'Bajo': 'Cuerdas',
            'Violín': 'Cuerdas',
            'Saxofón': 'Vientos',
            'Trompeta': 'Vientos',
            'Flauta': 'Vientos',
            'Guitarra Eléctrica': 'Cuerdas'
        }.get(obj.nombre, 'Otros')
    )


class GeneroFactory(django.DjangoModelFactory):
    """Factory para géneros musicales"""
    
    class Meta:
        model = Genero
        django_get_or_create = ('nombre',)
    
    nombre = fuzzy.FuzzyChoice([
        'Rock', 'Pop', 'Jazz', 'Blues', 'Reggae', 'Folk', 
        'Electronic', 'Classical', 'Country', 'Funk'
    ])
    descripcion = factory.LazyAttribute(
        lambda obj: f"Género musical {obj.nombre}"
    )


class NivelExperienciaFactory(django.DjangoModelFactory):
    """Factory para niveles de experiencia"""
    
    class Meta:
        model = NivelExperiencia
        django_get_or_create = ('nombre',)
    
    nombre = fuzzy.FuzzyChoice(['Principiante', 'Intermedio', 'Avanzado', 'Profesional'])
    descripcion = factory.LazyAttribute(
        lambda obj: f"Nivel {obj.nombre.lower()}"
    )
    orden = factory.LazyAttribute(
        lambda obj: {
            'Principiante': 1,
            'Intermedio': 2,
            'Avanzado': 3,
            'Profesional': 4
        }.get(obj.nombre, 1)
    )
    años_minimos = factory.LazyAttribute(
        lambda obj: {
            'Principiante': 0,
            'Intermedio': 2,
            'Avanzado': 5,
            'Profesional': 8
        }.get(obj.nombre, 0)
    )
    años_maximos = factory.LazyAttribute(
        lambda obj: {
            'Principiante': 1,
            'Intermedio': 4,
            'Avanzado': 7,
            'Profesional': None
        }.get(obj.nombre, None)
    )


class PerfilMusicoFactory(django.DjangoModelFactory):
    """Factory para perfiles de músico"""
    
    class Meta:
        model = PerfilMusico
    
    usuario = factory.SubFactory(MusicoFactory)
    telefono = factory.LazyFunction(lambda: f"+569{fake.random_int(min=10000000, max=99999999)}")
    fecha_nacimiento = factory.LazyFunction(
        lambda: fake.date_between(start_date='-60y', end_date='-18y')
    )
    direccion = factory.LazyFunction(fake.address)
    recibir_notificaciones_email = True
    mostrar_telefono_publico = False


class PerfilEmpleadorFactory(django.DjangoModelFactory):
    """Factory para perfiles de empleador"""
    
    class Meta:
        model = PerfilEmpleador
    
    usuario = factory.SubFactory(EmpleadorFactory)
    nombre_organizacion = factory.LazyFunction(fake.company)
    tipo_entidad = fuzzy.FuzzyChoice(['empresa', 'fundacion', 'particular'])
    descripcion = factory.LazyFunction(lambda: fake.text(max_nb_chars=300))
    telefono = factory.LazyFunction(
        lambda: f"+569{fake.random_int(min=10000000, max=99999999)}"
    )


class PortafolioFactory(django.DjangoModelFactory):
    """Factory para portafolios"""
    
    class Meta:
        model = Portafolio
    
    usuario = factory.SubFactory(MusicoFactory)
    biografia = factory.LazyFunction(
        lambda: fake.text(max_nb_chars=500)
    )
    formacion_musical = factory.LazyFunction(
        lambda: fake.text(max_nb_chars=300)
    )
    años_experiencia = fuzzy.FuzzyInteger(1, 20)
    ubicacion = factory.SubFactory(UbicacionFactory)
    nivel_experiencia = factory.SubFactory(NivelExperienciaFactory)
    website_personal = factory.LazyFunction(fake.url)
    tarifa_base = fuzzy.FuzzyInteger(50000, 500000, step=10000)
    disponible_para_gigs = True
    show_email = False
    show_social_links = True
    show_education = True
    show_tarifa = True
    show_telefono = False
    activo = True


class OfertaLaboralFactory(django.DjangoModelFactory):
    """Factory para ofertas laborales"""
    
    class Meta:
        model = OfertaLaboral
    
    empleador = factory.SubFactory(PerfilEmpleadorFactory)
    titulo = factory.LazyFunction(
        lambda: f"Busco {fake.job()} Musical"
    )
    descripcion = factory.LazyFunction(
        lambda: fake.text(max_nb_chars=500)
    )
    tipo_contrato = fuzzy.FuzzyChoice(['evento_unico', 'temporal', 'permanente'])
    ubicacion = factory.SubFactory(UbicacionFactory)
    nivel_experiencia_minimo = factory.SubFactory(NivelExperienciaFactory)
    presupuesto_minimo = fuzzy.FuzzyInteger(50000, 300000, step=10000)
    presupuesto_maximo = factory.LazyAttribute(
        lambda obj: obj.presupuesto_minimo + fuzzy.FuzzyInteger(50000, 200000, step=10000).fuzz()
    )
    cupos_disponibles = fuzzy.FuzzyInteger(1, 5)
    estado = 'publicada'


class PortafolioInstrumentoFactory(django.DjangoModelFactory):
    """Factory para relación portafolio-instrumento"""
    
    class Meta:
        model = PortafolioInstrumento
    
    portafolio = factory.SubFactory(PortafolioFactory)
    instrumento = factory.SubFactory(InstrumentoFactory)
    nivel_dominio = fuzzy.FuzzyChoice(['principiante', 'intermedio', 'avanzado', 'profesional'])
    prioridad = fuzzy.FuzzyInteger(1, 5)


class PortafolioGeneroFactory(django.DjangoModelFactory):
    """Factory para relación portafolio-género"""
    
    class Meta:
        model = PortafolioGenero
    
    portafolio = factory.SubFactory(PortafolioFactory)
    genero = factory.SubFactory(GeneroFactory)
    prioridad = fuzzy.FuzzyInteger(1, 5)


class MultimediaFactory(django.DjangoModelFactory):
    """Factory para archivos multimedia"""
    
    class Meta:
        model = Multimedia
    
    portafolio = factory.SubFactory(PortafolioFactory)
    tipo = fuzzy.FuzzyChoice(['video', 'audio', 'imagen'])
    titulo = factory.LazyFunction(
        lambda: f"Sample {fake.word()}"
    )
    descripcion = factory.LazyFunction(fake.sentence)
    # Para testing, usamos URLs fake en lugar de archivos reales
    enlace_externo = factory.LazyFunction(
        lambda: f"https://example.com/media/{fake.uuid4()}"
    )
    activo = True
