#!/usr/bin/env python
"""
Script para verificar y completar perfiles existentes
"""

import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')
django.setup()

from usuarios.models import Usuario, Portafolio

def verificar_perfiles():
    """Verificar estado de los perfiles"""
    usernames = ['antoniavega', 'sebastianmorales', 'paulacontreras', 
                'javieralvarez', 'marcelatorres', 'tomasriquelme']
    
    for username in usernames:
        try:
            usuario = Usuario.objects.get(username=username)
            print(f"Usuario {username}: ✅ Existe")
            
            try:
                portafolio = Portafolio.objects.get(usuario=usuario)
                print(f"  Portafolio: ✅ Existe (ID: {portafolio.id})")
                print(f"  Biografía: {portafolio.biografia[:50]}...")
                print(f"  Instrumentos: {portafolio.portafolio_instrumentos.count()}")
                print(f"  Géneros: {portafolio.portafolio_generos.count()}")
            except Portafolio.DoesNotExist:
                print(f"  Portafolio: ❌ No existe")
                
        except Usuario.DoesNotExist:
            print(f"Usuario {username}: ❌ No existe")
        
        print()

def limpiar_usuarios_incompletos():
    """Eliminar usuarios que se crearon sin datos completos"""
    usernames = ['antoniavega', 'sebastianmorales', 'paulacontreras', 
                'javieralvarez', 'marcelatorres', 'tomasriquelme']
    
    for username in usernames:
        try:
            usuario = Usuario.objects.get(username=username)
            try:
                portafolio = Portafolio.objects.get(usuario=usuario)
                if not portafolio.biografia or portafolio.portafolio_instrumentos.count() == 0:
                    print(f"Eliminando usuario incompleto: {username}")
                    usuario.delete()
                else:
                    print(f"Usuario {username} está completo, manteniéndolo")
            except Portafolio.DoesNotExist:
                print(f"Eliminando usuario sin portafolio: {username}")
                usuario.delete()
        except Usuario.DoesNotExist:
            print(f"Usuario {username} no existe")

if __name__ == "__main__":
    print("🔍 Verificando perfiles existentes...")
    verificar_perfiles()
    
    print("🧹 Limpiando usuarios incompletos...")
    limpiar_usuarios_incompletos()
    
    print("✅ Verificación completada")
