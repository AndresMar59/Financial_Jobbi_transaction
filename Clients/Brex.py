from pathlib import Path
from urllib import response
import uuid 
import requests
from dotenv import load_dotenv
import os

load_dotenv()


# No es necesario la clase, dado que solo hay un token. La instancia no ocupa parametro
class BrexClient:
    BASE_URL = "https://api.brex.com" # Sin la barra al final para controlar mejor

    def __init__(self):
# Esto calcula la ruta a la raíz del proyecto (un nivel arriba de Clients/)
        base_dir = Path(__file__).resolve().parent.parent
        env_path = base_dir / '.env'
        
        # Cargamos el archivo especificando la ruta exacta
        load_dotenv(dotenv_path=env_path)
        
        token = os.getenv("BREX_TOK")

        if not token:
            print(f"ERROR: No se encontró el .env en: {env_path}")
        else:
            print(f"Token cargado correctamente")
            
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

    def paginated(self, ruta, params=None):
        if params is None:
            params = {}
            
        all_results = []
        next_cursor = None
        
        # Limpiamos la ruta por si trae una barra inicial

        while True:
            query_params = params.copy()
            if next_cursor:
                query_params["cursor"] = next_cursor

            # Construcción de URL segura
            full_url = f"{self.BASE_URL}/{ruta}"
            
            response = requests.get(
                full_url,
                headers=self.headers,
                params=query_params,
            )

            if response.status_code != 200:
                # Si es 401, imprimimos el header (sin el token completo por seguridad)
                if response.status_code == 401:
                    print(f"Header enviado: Bearer {str(os.getenv('BREX_TOK'))[:5]}...")
                raise Exception(f"Brex Error {response.status_code}: {response.text}")

            data_json = response.json()
            all_results.extend(data_json.get("items", []))

            next_cursor = data_json.get("next_cursor")
            if not next_cursor:
                break

        return all_results

    def get_Icome_paginated(self, params, ruta, id:str):
        """
        Llama a Brex y resuelve la paginación correctamente.
        """
        all_results = []
        next_cursor = None
        # La API de Brex usa paginación por cursor.
        while True:
            query_params = params.copy()

            if next_cursor:
                query_params["cursor"] = next_cursor

            response = requests.get( f"{self.BASE_URL}{ruta}",
                headers=self.headers,
                params=query_params,
            )

            print("STATUS:", response.status_code)
            print("RAW TEXT:", response.text[:500])

            if response.status_code != 200:
                raise Exception(
                    f"Error desde Brex: {response.status_code} - {response.text}"
                )

            try:
                data_json = response.json()
            except:
                raise Exception(f"Brex no devolvió JSON válido: {response.text}")

            # La data viene en: data_json["items"]
            items = data_json.get("items", [])
            all_results.extend(items)

            # Cursor correcto viene en: data_json["next_cursor"]
            next_cursor = data_json.get("next_cursor")
            if not next_cursor:
                break

        return all_results
    
    def post_webhook(self, api= str, payload = dict):

        full_url = f"{self.BASE_URL}/{api}"
            
        response = requests.post(
                full_url,
                json=payload,
                headers=self.headers,
            )
        
        return response
    
    def bloquear_tarjeta_en_brex(self, id_tarjeta: str):
        endpoint = f"v2/cards/{id_tarjeta}/lock"
        full_url = f"{self.BASE_URL}/{endpoint}"
        
        headers = self.headers.copy()
        headers["Idempotency-Key"] = str(uuid.uuid4())
        
        # El payload que pide Brex para bloquear el estado
        payload = {
            "description": "Fraude de tarjeta",
            "reason": "FRAUD"
        }
        
        print(f"Solicitando bloqueo en Brex para la tarjeta: {id_tarjeta}...")
        
        response = requests.post(full_url, json=payload, headers=headers)
        return response








    

