from django.core.mail import send_mail
from datetime import datetime

class Auditoria():

    def __init__(self, alerta = list, dia=None):
        self.alertas = alerta        
        # Si no te pasan un día, tomamos el día numérico actual por defecto
        self.hoy = dia if dia is not None else datetime.now().day
        
    def handle(self): 

        lista = self.alertas       

        if not lista:
            print("Todo en orden. No hay alertas estadísticas.")
            return False  # Retornamos False para saber que no hay anomalías

        mensaje = f"Se detectaron {len(lista)} gastos raros hoy {datetime.now().strftime('%d/%m/%Y')}:\n\n"
        
        for a in lista:
            # Manejo seguro de None en Z-Scores por si el comercio tiene < 3 meses
            z_m_val = float(a['z_monto']) if a['z_monto'] is not None else 0.0
            z_f_val = float(a['z_frecuencia']) if a['z_frecuencia'] is not None else 0.0

            mensaje += f"----------------------------------\n"
            mensaje += f"PLATAFORMA: {a['name']} (ID: {a['merchant_id']})\n"
            mensaje += f"USUARIO: {a['usuario']}\n"
            mensaje += f"MONTO ACTUAL: {float(a['monto_actual']):.2f}\n"
            mensaje += f"AVG MONTO: {float(a['avg_monto']):.2f}\n"
            mensaje += f"Z-SCORE MONTO: {z_m_val:.2f}\n"
            mensaje += f"FRECUENCIA: {float(a['frecuencia_actual']):.2f}\n"
            mensaje += f"AVG FRECUENCIA: {float(a['avg_frecuencia']):.2f}\n"
            mensaje += f"Z-SCORE FRECUENCIA: {z_f_val:.2f}\n"
            mensaje += f"----------------------------------\n\n"

        # 4. Enviar el correo de notificación
        try:
            send_mail(
                subject='ALERTA GASTOS RAROS DETECTADOS',
                message=mensaje,
                from_email=None,  # Toma el DEFAULT_FROM_EMAIL de tu settings.py
                recipient_list=['andres@jobbi.me'],
                fail_silently=False,
            )
            print("Correo enviado exitosamente.")
            return True  # Retornamos True indicando que sí se gatilló una alerta crítica
        except Exception as e:
            print(f"Error enviando correo: {e}")
            return True