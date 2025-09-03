#!/usr/bin/env python
"""
Script para crear perfiles de músicos específicos
"""

import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from usuarios.models import (
    Usuario, PerfilMusico, Portafolio, Instrumento, Genero, 
    NivelExperiencia, Ubicacion, PortafolioInstrumento, PortafolioGenero
)

def crear_o_obtener_datos_base():
    """Crear o obtener datos base necesarios"""
    
    # Niveles de experiencia
    niveles = {
        'Intermedio': NivelExperiencia.objects.get_or_create(nombre='Intermedio')[0],
        'Avanzado': NivelExperiencia.objects.get_or_create(nombre='Avanzado')[0],
        'Profesional': NivelExperiencia.objects.get_or_create(nombre='Profesional')[0],
    }
    
    # Ubicaciones
    ubicaciones = {
        'Santiago': Ubicacion.objects.get_or_create(nombre='Santiago')[0],
        'Providencia': Ubicacion.objects.get_or_create(nombre='Providencia')[0],
        'Ñuñoa': Ubicacion.objects.get_or_create(nombre='Ñuñoa')[0],
        'Santiago Centro': Ubicacion.objects.get_or_create(nombre='Santiago Centro')[0],
        'Maipú': Ubicacion.objects.get_or_create(nombre='Maipú')[0],
    }
    
    # Instrumentos
    instrumentos = {
        'Violín': Instrumento.objects.get_or_create(nombre='Violín')[0],
        'Viola': Instrumento.objects.get_or_create(nombre='Viola')[0],
        'Guitarra acústica': Instrumento.objects.get_or_create(nombre='Guitarra acústica')[0],
        'Guitarra eléctrica': Instrumento.objects.get_or_create(nombre='Guitarra eléctrica')[0],
        'Coros': Instrumento.objects.get_or_create(nombre='Coros')[0],
        'Voz': Instrumento.objects.get_or_create(nombre='Voz')[0],
        'Piano': Instrumento.objects.get_or_create(nombre='Piano')[0],
        'Saxofón': Instrumento.objects.get_or_create(nombre='Saxofón')[0],
        'Clarinete': Instrumento.objects.get_or_create(nombre='Clarinete')[0],
        'Flauta traversa': Instrumento.objects.get_or_create(nombre='Flauta traversa')[0],
        'Teclados': Instrumento.objects.get_or_create(nombre='Teclados')[0],
        'Synths': Instrumento.objects.get_or_create(nombre='Synths')[0],
        'Percusión latina': Instrumento.objects.get_or_create(nombre='Percusión latina')[0],
        'Cajón peruano': Instrumento.objects.get_or_create(nombre='Cajón peruano')[0],
        'Timbales': Instrumento.objects.get_or_create(nombre='Timbales')[0],
    }
    
    # Géneros
    generos = {
        'Folk': Genero.objects.get_or_create(nombre='Folk')[0],
        'Clásico': Genero.objects.get_or_create(nombre='Clásico')[0],
        'Rock': Genero.objects.get_or_create(nombre='Rock')[0],
        'Indie': Genero.objects.get_or_create(nombre='Indie')[0],
        'Blues': Genero.objects.get_or_create(nombre='Blues')[0],
        'Jazz': Genero.objects.get_or_create(nombre='Jazz')[0],
        'Bossa': Genero.objects.get_or_create(nombre='Bossa')[0],
        'Pop': Genero.objects.get_or_create(nombre='Pop')[0],
        'Funk': Genero.objects.get_or_create(nombre='Funk')[0],
        'Urbano': Genero.objects.get_or_create(nombre='Urbano')[0],
        'Electrónica': Genero.objects.get_or_create(nombre='Electrónica')[0],
        'Salsa': Genero.objects.get_or_create(nombre='Salsa')[0],
        'Timba': Genero.objects.get_or_create(nombre='Timba')[0],
        'Latin Jazz': Genero.objects.get_or_create(nombre='Latin Jazz')[0],
    }
    
    return niveles, ubicaciones, instrumentos, generos

def crear_perfil_musico(datos_usuario, datos_perfil, datos_portafolio):
    """Crear un perfil completo de músico"""
    
    print(f"Creando perfil: {datos_usuario['username']}")
    
    try:
        # Verificar si el usuario ya existe
        if Usuario.objects.filter(username=datos_usuario['username']).exists():
            print(f"  ⚠️  Usuario {datos_usuario['username']} ya existe, omitiendo...")
            return
        
        # Crear usuario
        usuario = Usuario.objects.create(
            username=datos_usuario['username'],
            email=datos_usuario['email'],
            password=make_password(datos_usuario['password']),
            first_name=datos_usuario['first_name'],
            last_name=datos_usuario['last_name'],
            tipo_usuario='musico'
        )
        
        # Crear perfil músico
        perfil = PerfilMusico.objects.create(
            usuario=usuario,
            **datos_perfil
        )
        
        # Crear portafolio (sin instrumento_principal)
        portafolio_data = datos_portafolio['base'].copy()
        instrumento_principal = portafolio_data.pop('instrumento_principal')
        
        portafolio = Portafolio.objects.create(
            usuario=usuario,
            **portafolio_data
        )
        
        # Agregar instrumento principal
        PortafolioInstrumento.objects.create(
            portafolio=portafolio,
            instrumento=instrumento_principal,
            es_principal=True,
            prioridad=1
        )
        
        # Agregar instrumentos secundarios
        prioridad = 2
        for instrumento in datos_portafolio['instrumentos_secundarios']:
            PortafolioInstrumento.objects.create(
                portafolio=portafolio,
                instrumento=instrumento,
                es_principal=False,
                prioridad=prioridad
            )
            prioridad += 1
        
        # Agregar géneros musicales
        for genero in datos_portafolio['generos']:
            PortafolioGenero.objects.create(
                portafolio=portafolio,
                genero=genero
            )
        
        print(f"  ✅ Perfil {datos_usuario['username']} creado exitosamente")
        
    except Exception as e:
        print(f"  ❌ Error creando {datos_usuario['username']}: {e}")

def main():
    """Función principal"""
    print("🎵 Creando perfiles de músicos...")
    print("=" * 50)
    
    # Obtener datos base
    niveles, ubicaciones, instrumentos, generos = crear_o_obtener_datos_base()
    
    # Definir perfiles a crear
    perfiles = [
        {
            'usuario': {
                'username': 'antoniavega',
                'email': 'antonia.vega@example.com',
                'password': 'Passw0rd!234',
                'first_name': 'Antonia',
                'last_name': 'Vega'
            },
            'perfil': {
                'telefono': '+56912345678',
                'fecha_nacimiento': '1990-05-15'
            },
            'portafolio': {
                'base': {
                    'biografia': 'Violinista de fusión y folclor. Arreglos para cuerdas y presentaciones en eventos. Amplificación propia.',
                    'formacion_musical': 'Formación clásica y talleres de fusión folklórica; música de cámara.',
                    'años_experiencia': 9,
                    'nivel_experiencia': niveles['Profesional'],
                    'ubicacion': ubicaciones['Santiago'],
                    'instrumento_principal': instrumentos['Violín'],
                    'tarifa_base': 100000,
                    'disponible_para_gigs': True,
                    'website_personal': 'https://antoniavega.example.com',
                    'youtube_url': 'https://youtube.com/@antoniavegaviolin',
                    'soundcloud_url': 'https://soundcloud.com/antoniavega',
                    'spotify_url': 'https://open.spotify.com/artist/antoniavega',
                    'instagram_url': 'https://instagram.com/antonia.vega.violin',
                    'facebook_url': 'https://facebook.com/AntoniaVegaViolin',
                    'video_demo': 'https://youtu.be/VIOLINantovega',
                    'show_social_links': True,
                    'show_email': True,
                    'show_tarifa': True,
                    'show_telefono': True,
                    'show_education': True
                },
                'instrumentos_secundarios': [instrumentos['Viola'], instrumentos['Guitarra acústica']],
                'generos': [generos['Folk'], generos['Clásico']]
            }
        },
        {
            'usuario': {
                'username': 'sebastianmorales',
                'email': 'sebastian.morales@example.com',
                'password': 'Passw0rd!234',
                'first_name': 'Sebastián',
                'last_name': 'Morales'
            },
            'perfil': {
                'telefono': '+56987654321',
                'fecha_nacimiento': '1992-08-22'
            },
            'portafolio': {
                'base': {
                    'biografia': 'Guitarrista eléctrico para rock/indie. Experiencia en escenarios medianos y estudios caseros. Sesionista y reemplazos.',
                    'formacion_musical': 'Clases particulares y talleres de improvisación; curso de audio básico.',
                    'años_experiencia': 7,
                    'nivel_experiencia': niveles['Avanzado'],
                    'ubicacion': ubicaciones['Santiago'],
                    'instrumento_principal': instrumentos['Guitarra eléctrica'],
                    'tarifa_base': 95000,
                    'disponible_para_gigs': True,
                    'website_personal': 'https://sebastianmoralesgtr.example.com',
                    'youtube_url': 'https://youtube.com/@sebastianmoralesgtr',
                    'soundcloud_url': 'https://soundcloud.com/sebastianmorales',
                    'spotify_url': 'https://open.spotify.com/artist/sebastianmorales',
                    'instagram_url': 'https://instagram.com/seba.morales.gtr',
                    'facebook_url': 'https://facebook.com/SebastianMoralesGuitar',
                    'video_demo': 'https://youtu.be/GTRsebastian',
                    'show_social_links': True,
                    'show_email': True,
                    'show_tarifa': True,
                    'show_telefono': True,
                    'show_education': True
                },
                'instrumentos_secundarios': [instrumentos['Guitarra acústica'], instrumentos['Coros']],
                'generos': [generos['Rock'], generos['Indie'], generos['Blues']]
            }
        },
        {
            'usuario': {
                'username': 'paulacontreras',
                'email': 'paula.contreras@example.com',
                'password': 'Passw0rd!234',
                'first_name': 'Paula',
                'last_name': 'Contreras'
            },
            'perfil': {
                'telefono': '+56956789123',
                'fecha_nacimiento': '1988-03-10'
            },
            'portafolio': {
                'base': {
                    'biografia': 'Cantante de jazz/bossa con repertorio estándar y pop acústico. Experiencia en hoteles, eventos corporativos y festivales locales.',
                    'formacion_musical': 'Estudios en canto popular; armonía y ensamble jazz.',
                    'años_experiencia': 10,
                    'nivel_experiencia': niveles['Profesional'],
                    'ubicacion': ubicaciones['Providencia'],
                    'instrumento_principal': instrumentos['Voz'],
                    'tarifa_base': 110000,
                    'disponible_para_gigs': True,
                    'website_personal': 'https://paulacontrerasvoz.example.com',
                    'youtube_url': 'https://youtube.com/@paulacontrerasvoz',
                    'soundcloud_url': 'https://soundcloud.com/paulacontreras',
                    'spotify_url': 'https://open.spotify.com/artist/paulacontreras',
                    'instagram_url': 'https://instagram.com/paula.contreras.voz',
                    'facebook_url': 'https://facebook.com/PaulaContrerasVoz',
                    'video_demo': 'https://youtu.be/VOZpaula',
                    'show_social_links': True,
                    'show_email': True,
                    'show_tarifa': True,
                    'show_telefono': True,
                    'show_education': True
                },
                'instrumentos_secundarios': [instrumentos['Piano'], instrumentos['Coros']],
                'generos': [generos['Jazz'], generos['Bossa'], generos['Pop']]
            }
        },
        {
            'usuario': {
                'username': 'javieralvarez',
                'email': 'javier.alvarez@example.com',
                'password': 'Passw0rd!234',
                'first_name': 'Javier',
                'last_name': 'Álvarez'
            },
            'perfil': {
                'telefono': '+56923456789',
                'fecha_nacimiento': '1989-11-07'
            },
            'portafolio': {
                'base': {
                    'biografia': 'Saxofonista para jazz/funk/pop. Sesionista, arreglos de vientos y trabajos en estudio. Lectura fluida.',
                    'formacion_musical': 'Conservatorio (saxo); seminarios de improvisación moderna.',
                    'años_experiencia': 8,
                    'nivel_experiencia': niveles['Avanzado'],
                    'ubicacion': ubicaciones['Ñuñoa'],
                    'instrumento_principal': instrumentos['Saxofón'],
                    'tarifa_base': 120000,
                    'disponible_para_gigs': True,
                    'website_personal': 'https://javieralvarezsax.example.com',
                    'youtube_url': 'https://youtube.com/@javieralvarezsax',
                    'soundcloud_url': 'https://soundcloud.com/javieralvarez',
                    'spotify_url': 'https://open.spotify.com/artist/javieralvarez',
                    'instagram_url': 'https://instagram.com/javier.alvarez.sax',
                    'facebook_url': 'https://facebook.com/JavierAlvarezSax',
                    'video_demo': 'https://youtu.be/SAXjavier',
                    'show_social_links': True,
                    'show_email': True,
                    'show_tarifa': True,
                    'show_telefono': True,
                    'show_education': True
                },
                'instrumentos_secundarios': [instrumentos['Clarinete'], instrumentos['Flauta traversa']],
                'generos': [generos['Jazz'], generos['Funk'], generos['Pop']]
            }
        },
        {
            'usuario': {
                'username': 'marcelatorres',
                'email': 'marcela.torres@example.com',
                'password': 'Passw0rd!234',
                'first_name': 'Marcela',
                'last_name': 'Torres'
            },
            'perfil': {
                'telefono': '+56934567890',
                'fecha_nacimiento': '1995-06-18'
            },
            'portafolio': {
                'base': {
                    'biografia': 'Tecladista para pop/urbano con experiencia en pistas, samples y refuerzos armónicos. Trabajo con MainStage/Ableton.',
                    'formacion_musical': 'Cursos de producción musical y performance con DAW.',
                    'años_experiencia': 4,
                    'nivel_experiencia': niveles['Intermedio'],
                    'ubicacion': ubicaciones['Santiago Centro'],
                    'instrumento_principal': instrumentos['Teclados'],
                    'tarifa_base': 90000,
                    'disponible_para_gigs': True,
                    'website_personal': 'https://marcelatorressynth.example.com',
                    'youtube_url': 'https://youtube.com/@marcelatorreskeys',
                    'soundcloud_url': 'https://soundcloud.com/marcelatorres',
                    'spotify_url': 'https://open.spotify.com/artist/marcelatorres',
                    'instagram_url': 'https://instagram.com/marcela.torres.keys',
                    'facebook_url': 'https://facebook.com/MarcelaTorresKeys',
                    'video_demo': 'https://youtu.be/SYNmarcela',
                    'show_social_links': True,
                    'show_email': True,
                    'show_tarifa': True,
                    'show_telefono': True,
                    'show_education': True
                },
                'instrumentos_secundarios': [instrumentos['Piano'], instrumentos['Synths']],
                'generos': [generos['Pop'], generos['Urbano'], generos['Electrónica']]
            }
        },
        {
            'usuario': {
                'username': 'tomasriquelme',
                'email': 'tomas.riquelme@example.com',
                'password': 'Passw0rd!234',
                'first_name': 'Tomás',
                'last_name': 'Riquelme'
            },
            'perfil': {
                'telefono': '+56945678901',
                'fecha_nacimiento': '1986-12-03'
            },
            'portafolio': {
                'base': {
                    'biografia': 'Percusionista latino con amplia experiencia en salsa/timba. Refuerzos de vientos y secciones rítmicas en escenarios grandes.',
                    'formacion_musical': 'Clases con percusionistas cubanos; talleres de ritmos afrolatinos.',
                    'años_experiencia': 12,
                    'nivel_experiencia': niveles['Profesional'],
                    'ubicacion': ubicaciones['Maipú'],
                    'instrumento_principal': instrumentos['Percusión latina'],
                    'tarifa_base': 100000,
                    'disponible_para_gigs': True,
                    'website_personal': 'https://tomasriquelmeperc.example.com',
                    'youtube_url': 'https://youtube.com/@tomasriquelmeperc',
                    'soundcloud_url': 'https://soundcloud.com/tomasriquelme',
                    'spotify_url': 'https://open.spotify.com/artist/tomasriquelme',
                    'instagram_url': 'https://instagram.com/tomas.riquelme.perc',
                    'facebook_url': 'https://facebook.com/TomasRiquelmePerc',
                    'video_demo': 'https://youtu.be/PERCtomas',
                    'show_social_links': True,
                    'show_email': True,
                    'show_tarifa': True,
                    'show_telefono': True,
                    'show_education': True
                },
                'instrumentos_secundarios': [instrumentos['Cajón peruano'], instrumentos['Timbales']],
                'generos': [generos['Salsa'], generos['Timba'], generos['Latin Jazz']]
            }
        }
    ]
    
    # Crear cada perfil
    for perfil_data in perfiles:
        crear_perfil_musico(
            perfil_data['usuario'],
            perfil_data['perfil'],
            perfil_data['portafolio']
        )
    
    print("=" * 50)
    print("🎉 Proceso completado!")
    print(f"Total usuarios creados: {len([p for p in perfiles if not Usuario.objects.filter(username=p['usuario']['username']).exists()])}")

if __name__ == "__main__":
    main()
