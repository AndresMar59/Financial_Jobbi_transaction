import sys
import os

# Esto fuerza a Python a incluir la carpeta raíz 'Compras' en sus rutas de búsqueda
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Clients.Brex import BrexClient


def registrar_nuestro_webhook():
    # 1. Tu URL pública de Ngrok apuntando a tu endpoint de Django
    url_ngrok = "https://financialjobbitransaction-production.up.railway.app/api/webhooks/brex-receiver/"
    
    # 2. Los datos de la suscripción (El mismo Body de la documentación)
    payload = {
        "url": url_ngrok,
        "event_types": [
            "EXPENSE_PAYMENT_UPDATED",
        ]
    }

    mi_llave_idempotente = "mi-llave-registro-webhook-v2"
    
    client = BrexClient()
    client.headers["Idempotency-Key"] = mi_llave_idempotente
    print(f" La Idempotency-Key que estamos mandando es: {mi_llave_idempotente}")
    print("Enviando solicitud de registro a Brex...")
    
    try:
        # Usamos un POST directo al endpoint de webhooks de Brex
        response = client.post_webhook(api="v1/webhooks", payload=payload)
        
        print("Respuesta de Brex:", response)
        
        # Si tu método devuelve la respuesta cruda de requests, puedes ver el JSON así:
        if hasattr(response, "json"):
            print("JSON de respuesta:", response.json())
            
    except Exception as e:
        print("\n❌ Error al registrar el webhook:")
        print(str(e))
        
if __name__ == "__main__":
    registrar_nuestro_webhook()