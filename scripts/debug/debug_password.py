#!/usr/bin/env python
"""
Script para debuggear el test de recuperación de password
"""

import os
import sys
import django

# Configurar Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetandgig.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.messages import get_messages

def debug_recuperar_password():
    """Debug del comportamiento de recuperar password"""
    print("🔍 Debuggeando recuperación de password con email inexistente...")
    
    client = Client()
    form_data = {
        'email': 'noexiste@example.com',
    }
    
    response = client.post(reverse('recuperar_password'), data=form_data, follow=True)
    
    print(f"Status code: {response.status_code}")
    print(f"URL final: {response.request['PATH_INFO']}")
    
    # Verificar mensajes
    messages = list(get_messages(response.wsgi_request))
    print(f"Número de mensajes: {len(messages)}")
    
    for i, message in enumerate(messages):
        print(f"Mensaje {i+1}: '{message}' (Tipo: {message.tags})")
    
    # Verificar contenido de la respuesta
    content = response.content.decode('utf-8')
    if 'No existe un usuario' in content:
        print("✅ El mensaje de error está en el contenido HTML")
    else:
        print("❌ El mensaje de error NO está en el contenido HTML")
        
    # Buscar otros patrones de mensaje
    possible_messages = [
        'No existe un usuario con este email',
        'Usuario no encontrado',
        'Email no registrado',
        'no existe',
        'inexistente'
    ]
    
    for pattern in possible_messages:
        if pattern.lower() in content.lower():
            print(f"✅ Encontrado patrón: '{pattern}'")

if __name__ == "__main__":
    debug_recuperar_password()
