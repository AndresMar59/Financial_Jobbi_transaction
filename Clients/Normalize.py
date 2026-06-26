import re
from difflib import SequenceMatcher
from Clients.models import Merchant, Expense

def normalize_merchant_name(name):
    if not name:
        return "unknown"
    
    # 1. Todo a minúsculas
    name = name.lower()
    
    name = re.sub(r'\*|\-|\_|([0-9]{3,})', ' ', name) # Se pone los '' espacios para evitar que palabras se peguen al eliminar caracteres o números
    
    noise = r'\b(www|com|inc|ltd|corp|software|services|srv|direct|checkout)\b' # Si se llama corporación, no lo queremos eliminar, pero si "corp" o "inc"
    name = re.sub(noise, '', name)
    
    # 4. Limpiar espacios extra y caracteres no alfanuméricos
    name = re.sub(r'[^a-z\s]', '', name)
    
    # 5. Trim y dejar un solo espacio entre palabras
    # Esto también ayuda a normalizar casos como "Starbucks Coffee" vs "Starbucks Coffee"
    return " ".join(name.split())


def probabilidad_cadenas_iguales(cadena1: str, cadena2: str) -> float:

    # Validación de entrada
    if not isinstance(cadena1, str) or not isinstance(cadena2, str):
        raise ValueError("Ambos parámetros deben ser cadenas de texto (str).")
    
    # Normalizamos espacios y pasamos a minúsculas para comparación más justa
    cadena1 = cadena1.strip().lower()
    cadena2 = cadena2.strip().lower()
    
    # Calculamos la similitud
    similitud = SequenceMatcher(True, cadena1, cadena2).ratio()
    return similitud


def normalize_category(brex_category):
    # Diccionario de mapeo: Brex Category -> Tu Categoria
    mapping = {
        'Software': 'SaaS',
        'SaaS': 'SaaS',
        'Professional Services': 'SaaS', # Herramientas como consultorías
        'Digital Advertising': 'Marketing',
        'Advertising': 'Marketing',
        'Travel': 'Ignore',
        'Restaurants': 'Ignore'
    }
    return mapping.get(brex_category, 'Other')


def obtener_similar(nombre_nuevo, threshold=0.75):
    """
    Busca en la DB un merchant con nombre similar.
    Retorna el objeto Merchant si lo encuentra, de lo contrario None.
    """
    merchants = Merchant.objects.all()
    for m in merchants:
        # Comparamos el nombre ya limpio de la DB con el nombre nuevo

        # IsJunk espera una funcion. Si el caracter es un espacio, lo ignora en la comparación.
        similitud = SequenceMatcher(lambda x: x == " ", m.clean_name, nombre_nuevo).ratio()
        if similitud > threshold:
            return m
    return None