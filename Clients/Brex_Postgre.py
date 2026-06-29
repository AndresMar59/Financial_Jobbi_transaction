from datetime import datetime, timedelta
from Clients.Brex import BrexClient
from dotenv import load_dotenv
from django.utils.dateparse import parse_datetime
from django.utils import timezone

load_dotenv()


def Costos_Total():

    parametros_expansion = {
        "expand[]": ["merchant", "location", "user", "department"],
        "status": "APPROVED",
        "payment_status": "CLEARED"
    }
    client = BrexClient()
    expenses_card = client.paginated("v1/expenses/card", params=parametros_expansion)

    if not isinstance(expenses_card, list):
        return []

    gastos_normalizados = []
    for gasto in expenses_card:

        p_status = gasto.get("payment_status")
        if p_status not in ["CLEARED", "POSTED"]: # Solo tomamos expenses que si se pagaron y de descontaron
            continue
        
        # Usamos .get() con fallback para evitar errores de NoneType
        gasto_id = gasto.get("id") # ID único de la transacción
        vendor_id = gasto.get("merchant_id") or "unknown"

        
        # Ojo: Brex a veces usa 'category' o 'category_group'
        category = (gasto.get("category") or "unknown").lower()
        
        merchant_obj = gasto.get("merchant") or {}
        name_vendor = merchant_obj.get("raw_descriptor", "unknown").lower()
        mcc = str(merchant_obj.get("mcc", "unknown")).lower()
        
        user_obj = gasto.get("user") or {}
        usuario = user_obj.get("first_name", "unknown")
        
        # Importante: Brex usa 'purchased_at'
        purchased_at = gasto.get("purchased_at", "0000-00-00")
        
        # Monto: Brex usualmente entrega 'original_amount' o 'amount'
        amount_data = gasto.get("original_amount") or {} # Ajusta según tu respuesta de Brex
        raw_amount = amount_data.get("amount", 0) / 100

        location_obj = gasto.get("location") or {}
        location_id = location_obj.get("id", "unknown")


        gastos_normalizados.append({
            "gasto_id": gasto_id,
            "vendor_brex_id": vendor_id,
            "amount": raw_amount,
            "date": purchased_at,
            "location": location_id,
            "address": (gasto.get("address") or {}).get("state", "unknown"),
            "mcc": mcc,
            "anio": purchased_at[:4],
            "mes": purchased_at[5:7],
            "usuario": usuario,
            "category": category,
            "name_vendor": name_vendor
        })
    return gastos_normalizados


def costo_diario():

    # Brex pide ISO 8601 completo para filtros de fecha
    ayer = datetime.now() - timedelta(days=1)
    # Formato: 2024-04-21T00:00:00Z
    fecha_iso = ayer.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

    parametros_expansion = {
        "expand[]": ["merchant", "location", "user", "department"],
        "purchased_at_start": fecha_iso,  # <-- CAMBIO CLAVE
        "status": "APPROVED"
    }
    client = BrexClient()
    expenses_card = client.paginated("v1/expenses/card", params=parametros_expansion)

    if not isinstance(expenses_card, list):
        return []

    gastos_normalizados = []
    for gasto in expenses_card:
        p_status = gasto.get("payment_status")
        if p_status not in ["CLEARED", "POSTED"]: # Solo tomamos expenses que si se pagaron y de descontaron
            continue

        # Usamos .get() con fallback para evitar errores de NoneType
        gasto_id = gasto.get("id") # ID único de la transacción
        vendor_id = gasto.get("merchant_id") or "unknown"
        
        # Ojo: Brex a veces usa 'category' o 'category_group'
        category = (gasto.get("category") or "unknown").lower()
        
        merchant_obj = gasto.get("merchant") or {}
        name_vendor = merchant_obj.get("raw_descriptor", "unknown").lower()
        mcc = str(merchant_obj.get("mcc", "unknown")).lower()
        
        user_obj = gasto.get("user") or {}
        usuario = user_obj.get("first_name", "unknown")
        
        # Importante: Brex usa 'purchased_at'
        purchased_at = gasto.get("purchased_at", "0000-00-00")
        
        # Monto: Brex usualmente entrega 'original_amount' o 'amount'
        amount_data = gasto.get("original_amount") or {} # Ajusta según tu respuesta de Brex
        raw_amount = amount_data.get("amount", 0) / 100

        location_obj = gasto.get("location") or {}
        location_id = location_obj.get("id", "unknown")


        gastos_normalizados.append({
            "gasto_id": gasto_id,
            "vendor_brex_id": vendor_id,
            "amount": raw_amount,
            "date": purchased_at,
            "location": location_id,
            "address": (gasto.get("address") or {}).get("state", "unknown"),
            "mcc": mcc,
            "anio": purchased_at[:4],
            "mes": purchased_at[5:7],
            "usuario": usuario,
            "category": category,
            "name_vendor": name_vendor
        })
    return gastos_normalizados


def Costo_Total_byExpense(id_expense):

    parametros_expansion = {
        "expand[]": ["merchant", "location", "user", "department"],
        "status": "APPROVED",
        "payment_status": "CLEARED"
    }
    client = BrexClient()
    # Esto va a venir de Webhook el id_expenses
    expenses_card = client.paginated("v1/expenses/card/{id_expense}", params=parametros_expansion)

    if not isinstance(expenses_card, list):
        return []

    gastos_normalizados = []
    for gasto in expenses_card:

        p_status = gasto.get("payment_status")
        if p_status not in ["CLEARED", "POSTED"]: # Solo tomamos expenses que si se pagaron y de descontaron
            continue
        
        # Usamos .get() con fallback para evitar errores de NoneType
        gasto_id = gasto.get("id") # ID único de la transacción
        vendor_id = gasto.get("merchant_id") or "unknown"

        
        # Ojo: Brex a veces usa 'category' o 'category_group'
        category = (gasto.get("category") or "unknown").lower()
        
        merchant_obj = gasto.get("merchant") or {}
        name_vendor = merchant_obj.get("raw_descriptor", "unknown").lower()
        mcc = str(merchant_obj.get("mcc", "unknown")).lower()
        
        user_obj = gasto.get("user") or {}
        usuario = user_obj.get("first_name", "unknown")
        
        # Importante: Brex usa 'purchased_at'
        purchased_at = gasto.get("purchased_at", "0000-00-00")
        
        # Monto: Brex usualmente entrega 'original_amount' o 'amount'
        amount_data = gasto.get("original_amount") or {} # Ajusta según tu respuesta de Brex
        raw_amount = amount_data.get("amount", 0) / 100

        location_obj = gasto.get("location") or {}
        location_id = location_obj.get("id", "unknown")


        gastos_normalizados.append({
            "gasto_id": gasto_id,
            "vendor_brex_id": vendor_id,
            "amount": raw_amount,
            "date": purchased_at,
            "location": location_id,
            "address": (gasto.get("address") or {}).get("state", "unknown"),
            "mcc": mcc,
            "anio": purchased_at[:4],
            "mes": purchased_at[5:7],
            "usuario": usuario,
            "category": category,
            "name_vendor": name_vendor
        })
    return gastos_normalizados


def costo_Total_webhook(item):
    gastos_normalizados = []
    
    # 1. FILTRO DE ÉXITO: Validamos con las llaves reales de Brex
    # 'payment_status_reason' o 'payment_status' nos dicen si pasó con éxito
    status_gasto = item.get("payment_status_reason") or item.get("payment_status")
    
    # Solo procesamos si el pago fue aprobado o liquidado
    if status_gasto not in ["APPROVED", "CLEARED", "POSTED"]: 
        return gastos_normalizados 
        
    gasto_id = item.get("expense_id")  # CORREGIDO: antes era "id"
    
    # Brex no manda 'merchant_id' en la raíz, usamos 'unknown' o una combinación segura
    vendor_id = "unknown" 
    
    # Brex no manda 'category' en este webhook de pago, por ahora por defecto 'unknown'
    category = "unknown"
        
    # Extraemos metadata del comercio
    merchant_obj = item.get("merchant") or {}
    name_vendor = merchant_obj.get("raw_descriptor", "unknown").lower()
    mcc = str(merchant_obj.get("mcc", "unknown")).lower()
        
    # Brex no incluye el objeto 'user' en este webhook. Ponemos 'unknown'
    usuario = "unknown"
        
    raw_date = item.get("purchased_at", None)

    if raw_date:
     purchased_at = parse_datetime(raw_date)  

    if purchased_at is None:
        purchased_at = timezone.now()                # fallback seguro
    else:
     purchased_at = timezone.now()
        
    # 2. MONTO REAL: Estructura corregida para acceder a item['amount']['amount']
    amount_data = item.get("amount") or item.get("original_amount") or {} 
    raw_amount = float(amount_data.get("amount", 0)) / 100  
 
    # Brex no manda location ni address directos, extraemos el país del merchant como parche seguro
    location_id = "unknown"
    address_state = merchant_obj.get("country", "unknown") # Usamos el país ya que no viene el estado

    gastos_normalizados.append({
        "gasto_id": gasto_id,
        "vendor_brex_id": vendor_id,
        "amount": raw_amount,
        "date": purchased_at,
        "location": location_id,
        "address": address_state, 
        "mcc": mcc, 
        "anio": purchased_at[:4],      # Corta "2023" perfectamente
        "mes": purchased_at[5:7],     # Corta "01" perfectamente
        "usuario": usuario, 
        "category": category, 
        "name_vendor": name_vendor 
    })
    
    return gastos_normalizados
    




