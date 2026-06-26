from Clients.models import Merchant, Expense
from Clients.Normalize import normalize_category, normalize_merchant_name, obtener_similar
from Clients.Brex_Postgre import Costos_Total, Costo_Total_byExpense

mock_gastos_recientes = [
    {
        "gasto_id": "fake_001",
        "vendor_brex_id": "pmch_cln26otnw025w0oknbasksls4",
        "amount": 49.00,
        "date": "2026-04-20T00:00:00Z", # Obligatorio
        "location": "loc_001",
        "address": "Bogotá",
        "mcc": "5411",
        "anio": "2026",
        "mes": "04",
        "usuario": "Andres Martinez",
        "category": "software", # Obligatorio
        "name_vendor": "coresignal"
    },
    {
        "gasto_id": "fake_002",
        "vendor_brex_id": "NUEVO_999",
        "amount": 1250.00,
        "date": "2026-04-22T00:00:00Z",
        "location": "loc_002",
        "address": "Medellín",
        "mcc": "5732",
        "anio": "2026",
        "mes": "04",
        "usuario": "Felipe Clautier",
        "category": "electronics",
        "name_vendor": "algo super raro s.a.s"
    },
    {
        "gasto_id": "fake_003",
        "vendor_brex_id": "NUEVO_555",
        "amount": 15.00,
        "date": "2026-04-22T00:00:00Z",
        "location": "loc_003",
        "address": "Bogotá",
        "mcc": "5812",
        "anio": "2026",
        "mes": "04",
        "usuario": "Andres Martinez",
        "category": "food & beverages",
        "name_vendor": "tienda local bogota"
    }
]




def procesar_transaccion(item):

    nuevo_merchant = False
    raw_name = item['name_vendor']
    brex_id = item['vendor_brex_id']

    # Normaliza el nombre en casoq ue sea una misma empresa pero brex los identifica con distintos ids
    temp_clean = normalize_merchant_name(raw_name)
    
    # 1. Buscar o crear Merchant
    merchant_obj = Merchant.objects.filter(brex_id=brex_id).first()

    

    if not merchant_obj:
        merchant_obj = obtener_similar(temp_clean) 
        
        if not merchant_obj or merchant_obj.clean_name == "unknown":
            print(f"Creando nuevo Merchant: {raw_name}")

            # Si se tiene que crear. Para ahcer una contabilizacion al final, se puede retornar un flag indicando que se creo un nuevo merchant
            nuevo_merchant = True
            merchant_obj = Merchant.objects.create(
                brex_id=brex_id,
                raw_name=raw_name,
                category_group=item['category'],
                internal_category=normalize_category(item['category']),
                clean_name=temp_clean,
                usuario=item['usuario']
            )

    # 2. Crear el Gasto (Asegúrate que los nombres coincidan con tu modelo)
    expenses = Expense.objects.get_or_create(
        brex_id_unico=item['gasto_id'], 
        merchant=merchant_obj,
        amount=item['amount'],        # Ya viene dividido entre 100 desde Costos_Total
        date=item['date'],          # Usamos la llave 'date' definida arriba
        anio=item['anio'],
        mes=item['mes'],
        location=item['location'],
        adress=item['address'],     # Verifica si es 'adress' o 'address' en tu DB
        category=item['category'],
        mcc=item['mcc']
    )
    
    return nuevo_merchant, merchant_obj, expenses 


def inicializar_sistema():
    
    lista_merchant = list()
    lista_de_objetos_brex = Costos_Total()
    total = len(lista_de_objetos_brex) # Para pruebas, puedes usar mock_gastos_recientes en lugar de Costos_Total()
    print(f" Iniciando carga de {total} transacciones...")
    
    for indice, item in enumerate(lista_de_objetos_brex, 1):
        try:
            # Llamamos a la función de procesamiento seguro que definimos
            v =  procesar_transaccion(item)

            if v[0]: # Si se creó un nuevo merchant, lo agregamos a la lista de alertas
             lista_merchant.append(v) # Agregamos el objeto Merchant a la lista de alertas

            if indice % 10 == 0:
                print(f"Procesados {indice}/{total}...")
        except Exception as e:
            print(f"Error en item {indice} ({item.get('merchant_name')}): {e}")

            # La respuesta de cada m es una tupla
    resultado = sum(1 for m in lista_merchant if m[0] is True)

    return resultado, lista_merchant


