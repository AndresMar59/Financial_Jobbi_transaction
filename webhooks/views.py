import json
from Clients.models import Merchant, Expense
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from Clients.management.commands.ejecutar_auditoria import Auditoria
from Clients.Gastos_ati.BaseZScoreAnalyzer import BaseZScoreAnalyzer
from Clients.Brex_Postgre import costo_Total_webhook
from Clients.Ingest_items import procesar_transaccion
from datetime import datetime
from Clients.Brex import BrexClient
from Clients.management.commands.ejecutar_auditoria import Auditoria



@csrf_exempt 
def brex_webhook_receiver(request):

    # El webhook devuelve una respuesta tipo expenses. Preguntar a IA de brex la estructura si se ocupa
    if request.method != 'POST':
        return HttpResponse("Método no permitido", status=405)
    
    # Covertis la respuesto en json 
    payload = json.loads(request.body)

    # Sacas el id de card para blouearla si es necesario
    card = payload.get("card_id")

    # Lo convertis en un objeto listo para poder ingresar a la BD
    compra = costo_Total_webhook(payload)

    #Procesas la transaccion, Agrega la compra, y registra el merchant, si no existe
    # Te devuelve un bool, si es nuevo merchant, el objeto merchant y el objeto expenses.
    validador, merchant, Expense = procesar_transaccion(compra)

    # Si no se logra procesar el gasto, no hace nada del cogido
    if not merchant:
        return ("No se puedo procesar el registro de compra")
    

    # Seleccionamos el id del merchant que se asigna incrementalmente en la BD
    merchant_id = Expense[0].merchant_id

    # Inicializas la clase de score con el merchant del gasto
    client = BaseZScoreAnalyzer(merchant_id = merchant_id)


    dia = datetime.now().day

    # Creamos la evalucion de z-score sobre el gasto 
    # 1. Debe haber al menos tres meses de gastos pasados de ese merchat
    # 2. Tiene que tener un scroe demasiado alto para que se active
    evaluacion = client.analizar_gastos_unico(dia)

    # Si existe al menos un objeto de la lista ahcemos el proceso de bloqueo
    if evaluacion[0]   :
        user = BrexClient()

        # creamos la variable que simplemente contendria la respuesta del request

        bloqueo = user.bloquear_tarjeta_en_brex(card)

        # Mandamos el esquema de respuesta de evalaucion para mandar mandar el correo 
        # Ejecutamos la fucnion 
        Audi = Auditoria(alerta=evaluacion, dia=dia)
        Audi.handle()
    
    # Si no hay alerta solo crea el expense y el merchant si es nuevo.
    return JsonResponse({"status": "success", "alert_triggered": bool(evaluacion[0])}, status=200)
        


