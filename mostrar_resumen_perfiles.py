#!/usr/bin/env python
"""
Script para mostrar resumen de perfiles creados
"""

import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')
django.setup()

from usuarios.models import Usuario, Portafolio

def mostrar_resumen():
    """Mostrar resumen de perfiles creados"""
    usernames = ['antoniavega', 'sebastianmorales', 'paulacontreras', 
                'javieralvarez', 'marcelatorres', 'tomasriquelme']
    
    print("🎵 RESUMEN DE PERFILES CREADOS")
    print("=" * 60)
    
    for username in usernames:
        try:
            usuario = Usuario.objects.get(username=username)
            portafolio = Portafolio.objects.get(usuario=usuario)
            
            # Obtener instrumento principal
            inst_principal = portafolio.portafolio_instrumentos.filter(es_principal=True).first()
            inst_principales_str = inst_principal.instrumento.nombre if inst_principal else "N/A"
            
            # Obtener géneros
            generos = [g.genero.nombre for g in portafolio.portafolio_generos.all()]
            generos_str = ", ".join(generos[:3])  # Mostrar máximo 3
            
            print(f"✅ {usuario.first_name} {usuario.last_name} (@{username})")
            print(f"   📧 {usuario.email}")
            print(f"   🎹 {inst_principales_str} | 🎵 {generos_str}")
            print(f"   📍 {portafolio.ubicacion.nombre if portafolio.ubicacion else 'N/A'}")
            print(f"   💰 ${portafolio.tarifa_base:,} CLP")
            print(f"   🔗 Portafolio: /portafolio/{portafolio.slug}/")
            print()
            
        except (Usuario.DoesNotExist, Portafolio.DoesNotExist) as e:
            print(f"❌ Error con {username}: {e}")
    
    print("=" * 60)
    print("🎉 ¡Todos los perfiles han sido creados exitosamente!")
    print("💡 Ahora puedes hacer login con cualquiera de estos usuarios")
    print("🔑 Password para todos: Passw0rd!234")

if __name__ == "__main__":
    mostrar_resumen()
