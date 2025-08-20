#!/usr/bin/env python
"""
Script para debuggear el problema de redes sociales del portafolio
"""

import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')
django.setup()

from usuarios.models import Portafolio, Usuario
from usuarios.forms import PortafolioForm

def debug_redes_sociales():
    """Debug del problema de redes sociales"""
    print("🔍 Debuggeando redes sociales del portafolio...")
    
    # Obtener un usuario músico
    usuario = Usuario.objects.filter(tipo_usuario='musico').first()
    if not usuario:
        print("❌ No hay usuarios músicos en la BD")
        return
    
    print(f"Usuario encontrado: {usuario.username}")
    
    # Obtener o crear portafolio
    try:
        portafolio = Portafolio.objects.get(usuario=usuario)
        print(f"Portafolio encontrado: ID {portafolio.id}")
    except Portafolio.DoesNotExist:
        print("❌ No existe portafolio para este usuario")
        return
    
    # Verificar campos de redes sociales actuales
    print("\n📊 Estado actual de redes sociales:")
    print(f"  show_social_links: {portafolio.show_social_links}")
    print(f"  website_personal: '{portafolio.website_personal}'")
    print(f"  youtube_url: '{portafolio.youtube_url}'")
    print(f"  soundcloud_url: '{portafolio.soundcloud_url}'")
    print(f"  spotify_url: '{portafolio.spotify_url}'")
    print(f"  instagram_url: '{portafolio.instagram_url}'")
    print(f"  facebook_url: '{portafolio.facebook_url}'")
    
    # Verificar método get_enlaces_sociales
    enlaces = portafolio.get_enlaces_sociales()
    print(f"\n🔗 Enlaces sociales retornados por get_enlaces_sociales(): {len(enlaces)}")
    for i, enlace in enumerate(enlaces):
        print(f"  {i+1}. {enlace['nombre']}: {enlace['url']}")
    
    # Simular edición del formulario
    print("\n🧪 Simulando edición con datos de prueba...")
    form_data = {
        'biografia': portafolio.biografia or 'Biografía de prueba',
        'formacion_musical': portafolio.formacion_musical or 'Autodidacta',
        'años_experiencia': portafolio.años_experiencia,
        'nivel_experiencia': portafolio.nivel_experiencia.id if portafolio.nivel_experiencia else 1,
        'ubicacion': portafolio.ubicacion.id if portafolio.ubicacion else 1,
        'instrumento_principal': portafolio.instrumento_principal.id if portafolio.instrumento_principal else 1,
        'generos_musicales': [g.id for g in portafolio.generos_musicales.all()[:1]],  # Al menos uno
        'website_personal': 'https://ejemplo.com',
        'youtube_url': 'https://youtube.com/channel/test',
        'soundcloud_url': 'https://soundcloud.com/test',
        'spotify_url': 'https://open.spotify.com/artist/test',
        'instagram_url': 'https://instagram.com/test',
        'facebook_url': 'https://facebook.com/test',
        'show_social_links': True,
        'disponible_para_gigs': True,
        'show_email': True,
        'show_education': True,
        'show_tarifa': True,
        'show_telefono': True
    }
    
    # Verificar si el formulario es válido
    form = PortafolioForm(data=form_data, instance=portafolio)
    if form.is_valid():
        print("✅ Formulario válido")
        
        # Guardar los cambios
        portafolio_updated = form.save()
        print("✅ Portafolio guardado")
        
        # Verificar cambios después del guardado
        print("\n📊 Estado después del guardado:")
        print(f"  show_social_links: {portafolio_updated.show_social_links}")
        print(f"  website_personal: '{portafolio_updated.website_personal}'")
        print(f"  youtube_url: '{portafolio_updated.youtube_url}'")
        print(f"  soundcloud_url: '{portafolio_updated.soundcloud_url}'")
        print(f"  spotify_url: '{portafolio_updated.spotify_url}'")
        print(f"  instagram_url: '{portafolio_updated.instagram_url}'")
        print(f"  facebook_url: '{portafolio_updated.facebook_url}'")
        
        # Verificar método get_enlaces_sociales después del guardado
        enlaces_after = portafolio_updated.get_enlaces_sociales()
        print(f"\n🔗 Enlaces después del guardado: {len(enlaces_after)}")
        for i, enlace in enumerate(enlaces_after):
            print(f"  {i+1}. {enlace['nombre']}: {enlace['url']}")
            
    else:
        print("❌ Formulario inválido")
        print("Errores:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")

if __name__ == "__main__":
    debug_redes_sociales()
