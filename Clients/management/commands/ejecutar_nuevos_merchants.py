from django.core.mail import send_mail
from Clients.Ingest_items import procesar_transaccion, inicializar_sistema
from Clients.models import Merchant, Expense
from datetime import datetime

class New_merchant():
    help = 'Analiza anomalías y detecta nuevos merchants'

    def handle(self, *args, **options):
        # 1. Obtener el día actual para el análisis acumulado
        hoy = datetime.now().day
        self.stdout.write(f"Iniciando auditoría para el día {hoy}...")

        # 2. Ejecutar tu lógica
        alertas, merchant = inicializar_sistema()

        if not merchant:
            self.stdout.write(self.style.SUCCESS("No hay nuevos merchants."))
            return

        # 3. Construir el mensaje
        mensaje = f"Se detectaron {alertas} nuevos merchants hoy {datetime.now().strftime('%d/%m/%Y')}:\n\n"
        
        for m in merchant:
            mensaje += f"----------------------------------\n"
            mensaje += f"PLATAFORMA: {m[1].clean_name} (ID: {m[1].brex_id})\n"
            mensaje += f"USUARIO: {m[1].usuario}\n"
            mensaje += f"CATEGORIA: {m[1].internal_category}\n"
            mensaje += f"FECHA: {datetime.now().strftime('%d/%m/%Y')}\n"
            mensaje += f"----------------------------------\n\n"

        # 4. Enviar el correo
        try:
            send_mail(
                subject='ALERTA NUEVO/OS MERCHANT DETECTADOS',
                message=mensaje,
                from_email=None,
                recipient_list=['andres@jobbi.me'],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS("Correo enviado exitosamente."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error enviando correo: {e}"))