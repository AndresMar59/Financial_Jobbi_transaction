import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Clients.management.commands.ejecutar_auditoria import Auditoria
from Clients.Gastos_ati.BaseZScoreAnalyzer import BaseZScoreAnalyzer
from Clients.Brex_Postgre import costo_Total_webhook
from Clients.Ingest_items import procesar_transaccion
from datetime import datetime
from Clients.Brex import BrexClient


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

    if not compra:
        return JsonResponse({"status": "ignored", "reason": "estado no procesable"}, status=200)

    gasto_individual = compra[0]

    validador, merchant, Expense = procesar_transaccion(gasto_individual)

    if not merchant:
        return JsonResponse({"status": "error", "message": "No se pudo procesar el registro de compra"}, status=400)

    merchant_id = Expense[0].merchant_id
    client = BaseZScoreAnalyzer(merchant_id=merchant_id)
    dia = datetime.now().day
    evaluacion = client.analizar_gastos_unico(dia)

    if evaluacion:
        user = BrexClient()
        bloqueo = user.bloquear_tarjeta_en_brex(card)
        Audi = Auditoria(alerta=evaluacion, dia=dia)
        Audi.handle()

    alert_triggered = bool(evaluacion) and bool(evaluacion[0])
    return JsonResponse({"status": "success", "alert_triggered": alert_triggered}, status=200)


