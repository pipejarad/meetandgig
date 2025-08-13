from django.core.management.base import BaseCommand
from django.db import transaction
from usuarios.models import Instrumento, Genero, NivelExperiencia, Ubicacion


class Command(BaseCommand):
    help = 'Poblar catálogos con datos iniciales de instrumentos, géneros y ubicaciones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Eliminar datos existentes antes de poblar'
        )
        parser.add_argument(
            '--categoria',
            type=str,
            choices=['instrumentos', 'generos', 'niveles', 'ubicaciones'],
            help='Poblar solo una categoría específica'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🎵 Iniciando poblado de catálogos MeetAndGig...')
        )

        try:
            with transaction.atomic():
                if options['reset']:
                    self._reset_catalogos(options['categoria'])

                if not options['categoria'] or options['categoria'] == 'instrumentos':
                    self._poblar_instrumentos()
                
                if not options['categoria'] or options['categoria'] == 'generos':
                    self._poblar_generos()
                
                if not options['categoria'] or options['categoria'] == 'niveles':
                    self._poblar_niveles_experiencia()
                
                if not options['categoria'] or options['categoria'] == 'ubicaciones':
                    self._poblar_ubicaciones()

            self.stdout.write(
                self.style.SUCCESS('✅ Catálogos poblados exitosamente')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error poblando catálogos: {str(e)}')
            )
            raise

    def _reset_catalogos(self, categoria=None):
        self.stdout.write('🧹 Limpiando catálogos existentes...')
        
        if not categoria or categoria == 'instrumentos':
            Instrumento.objects.all().delete()
        if not categoria or categoria == 'generos':
            Genero.objects.all().delete()
        if not categoria or categoria == 'niveles':
            NivelExperiencia.objects.all().delete()
        if not categoria or categoria == 'ubicaciones':
            Ubicacion.objects.all().delete()

    def _poblar_instrumentos(self):
        self.stdout.write('🎸 Poblando instrumentos...')
        
        instrumentos_data = {
            'Cuerdas': [
                'Guitarra Clásica', 'Guitarra Eléctrica', 'Guitarra Acústica',
                'Bajo Eléctrico', 'Bajo Acústico', 'Violín', 'Viola', 'Violonchelo',
                'Contrabajo', 'Charango', 'Cuatro Venezolano', 'Mandolina',
                'Banjo', 'Ukulele'
            ],
            'Vientos': [
                'Flauta Traversa', 'Flauta Dulce', 'Clarinete', 'Saxofón Alto',
                'Saxofón Tenor', 'Trompeta', 'Trombón', 'Tuba', 'Corno Francés',
                'Quena', 'Zampoña', 'Armónica', 'Oboe', 'Fagot'
            ],
            'Percusión': [
                'Batería', 'Cajón Peruano', 'Congas', 'Bongos', 'Timbales',
                'Djembe', 'Bombo Legüero', 'Pandero', 'Charango', 'Maracas',
                'Claves', 'Güiro', 'Campanas Tubulares', 'Xilófono'
            ],
            'Teclas': [
                'Piano', 'Piano Eléctrico', 'Teclado Sintetizador', 'Órgano',
                'Acordeón', 'Bandoneón', 'Clavecín', 'Melódica'
            ],
            'Folclore Chileno': [
                'Guitarra Folclórica', 'Bombo Nortino', 'Kultrun', 'Trutruca',
                'Rabel', 'Tormento', 'Acordeón de Botones'
            ]
        }

        created_count = 0
        for categoria, instrumentos in instrumentos_data.items():
            for nombre in instrumentos:
                instrumento, created = Instrumento.objects.get_or_create(
                    nombre=nombre,
                    defaults={'categoria': categoria}
                )
                if created:
                    created_count += 1

        self.stdout.write(f'  ➤ {created_count} instrumentos creados')

    def _poblar_generos(self):
        self.stdout.write('🎭 Poblando géneros musicales...')
        
        generos_data = [
            {
                'nombre': 'Rock',
                'descripcion': 'Género musical caracterizado por el uso de guitarras eléctricas, bajo y batería'
            },
            {
                'nombre': 'Pop',
                'descripcion': 'Música popular contemporánea con estructuras melódicas pegajosas'
            },
            {
                'nombre': 'Jazz',
                'descripcion': 'Género musical que se caracteriza por la improvisación y la complejidad armónica'
            },
            {
                'nombre': 'Blues',
                'descripcion': 'Género musical vocal e instrumental basado en el uso de notas de blues'
            },
            {
                'nombre': 'Folclore Chileno',
                'descripcion': 'Música tradicional de Chile incluyendo cueca, tonada y vals chileno'
            },
            {
                'nombre': 'Nueva Canción',
                'descripcion': 'Movimiento musical latinoamericano de contenido social y político'
            },
            {
                'nombre': 'Cumbia',
                'descripcion': 'Género musical y baile folclórico tradicional de Colombia'
            },
            {
                'nombre': 'Salsa',
                'descripcion': 'Género musical bailable resultante de la síntesis del son cubano'
            },
            {
                'nombre': 'Reggae',
                'descripcion': 'Género musical que se desarrolló por primera vez en Jamaica'
            },
            {
                'nombre': 'Electrónica',
                'descripcion': 'Música que emplea instrumentos musicales electrónicos y tecnología'
            },
            {
                'nombre': 'Clásica',
                'descripcion': 'Música culta, música clásica, música docta o música erudita'
            },
            {
                'nombre': 'Bolero',
                'descripcion': 'Género musical de origen cubano, muy popular en toda América Latina'
            },
            {
                'nombre': 'Tango',
                'descripcion': 'Género musical y danza nacida en Argentina y Uruguay'
            },
            {
                'nombre': 'Bossa Nova',
                'descripcion': 'Género musical brasileño derivado del samba y influido por el jazz'
            },
            {
                'nombre': 'Reggaetón',
                'descripcion': 'Género musical procedente de Puerto Rico a finales de los años 1990'
            }
        ]

        created_count = 0
        for genero_data in generos_data:
            genero, created = Genero.objects.get_or_create(
                nombre=genero_data['nombre'],
                defaults={'descripcion': genero_data['descripcion']}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  ➤ {created_count} géneros creados')

    def _poblar_niveles_experiencia(self):
        self.stdout.write('🎓 Poblando niveles de experiencia...')
        
        niveles_data = [
            {
                'nombre': 'Principiante',
                'descripcion': 'Menos de 2 años de experiencia',
                'orden': 1,
                'años_minimos': 0,
                'años_maximos': 2
            },
            {
                'nombre': 'Intermedio',
                'descripcion': '2-5 años de experiencia musical',
                'orden': 2,
                'años_minimos': 2,
                'años_maximos': 5
            },
            {
                'nombre': 'Avanzado',
                'descripcion': '5-10 años de experiencia musical',
                'orden': 3,
                'años_minimos': 5,
                'años_maximos': 10
            },
            {
                'nombre': 'Profesional',
                'descripcion': 'Más de 10 años, formación académica o profesional',
                'orden': 4,
                'años_minimos': 10,
                'años_maximos': None
            }
        ]

        created_count = 0
        for nivel_data in niveles_data:
            nivel, created = NivelExperiencia.objects.get_or_create(
                nombre=nivel_data['nombre'],
                defaults={
                    'descripcion': nivel_data['descripcion'],
                    'orden': nivel_data['orden'],
                    'años_minimos': nivel_data['años_minimos'],
                    'años_maximos': nivel_data['años_maximos']
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'  ➤ {created_count} niveles de experiencia creados')

    def _poblar_ubicaciones(self):
        self.stdout.write('📍 Poblando ubicaciones...')
        
        ubicaciones_data = [
            # Región Metropolitana
            {'nombre': 'Santiago', 'region': 'Región Metropolitana', 'orden': 1},
            {'nombre': 'Las Condes', 'region': 'Región Metropolitana', 'orden': 2},
            {'nombre': 'Providencia', 'region': 'Región Metropolitana', 'orden': 3},
            {'nombre': 'Ñuñoa', 'region': 'Región Metropolitana', 'orden': 4},
            {'nombre': 'Maipú', 'region': 'Región Metropolitana', 'orden': 5},
            {'nombre': 'Puente Alto', 'region': 'Región Metropolitana', 'orden': 6},
            
            # Valparaíso
            {'nombre': 'Valparaíso', 'region': 'Región de Valparaíso', 'orden': 10},
            {'nombre': 'Viña del Mar', 'region': 'Región de Valparaíso', 'orden': 11},
            {'nombre': 'Quilpué', 'region': 'Región de Valparaíso', 'orden': 12},
            
            # Concepción
            {'nombre': 'Concepción', 'region': 'Región del Biobío', 'orden': 20},
            {'nombre': 'Talcahuano', 'region': 'Región del Biobío', 'orden': 21},
            {'nombre': 'Chillán', 'region': 'Región del Biobío', 'orden': 22},
            
            # Otras regiones principales
            {'nombre': 'La Serena', 'region': 'Región de Coquimbo', 'orden': 30},
            {'nombre': 'Antofagasta', 'region': 'Región de Antofagasta', 'orden': 40},
            {'nombre': 'Temuco', 'region': 'Región de La Araucanía', 'orden': 50},
            {'nombre': 'Puerto Montt', 'region': 'Región de Los Lagos', 'orden': 60},
        ]

        created_count = 0
        for ubicacion_data in ubicaciones_data:
            ubicacion, created = Ubicacion.objects.get_or_create(
                nombre=ubicacion_data['nombre'],
                defaults={
                    'region': ubicacion_data['region'],
                    'orden': ubicacion_data['orden'],
                    'pais': 'Chile',
                    'activo': True
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'  ➤ {created_count} ubicaciones creadas')
