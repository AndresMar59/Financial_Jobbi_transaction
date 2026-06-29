import numpy as np
from django.db import connection
from datetime import datetime

from Clients.models import Merchant


class BaseZScoreAnalyzer:

    def __init__(self, merchant_id=None):
        # 1. Identidad del Merchant (puede empezar en None si usas analizar_gastos)
        self.merchant_id = merchant_id
        
        # 2. Atributos que se llenarán dinámicamente durante el bucle
        self.clean_name = None
        self.usuario = None
        
        # 3. Reloj del sistema (Vital para que las queries SQL sepan qué año/mes es hoy)
        self.hoy = datetime.now()
        
        # Variables de conveniencia para no escribir self.hoy.year cada vez en las queries
        self.anio = self.hoy.year
        self.mes = self.hoy.month # Pasarlo a dos digitos 

    def get_dual_historical_data(self, day_limit = int):
        query = """
            SELECT SUM(amount), COUNT(id)
            FROM "Clients_expense"
            WHERE merchant_id = %s AND EXTRACT(DAY FROM date) <= %s
            AND (anio < %s OR (anio = %s AND mes < %s))
            GROUP BY anio, mes
        """ 
        params = [self.merchant_id, day_limit, self.hoy.year, self.hoy.year, self.hoy.month]
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
        # Retornamos dos listas: una de montos y otra de conteos
        montos = [float(row[0]) for row in rows]
        conteos = [float(row[1]) for row in rows]
        return montos, conteos

    def evaluate_merchant(self, day_limit = int):
        # 1. Traer historial
        hist_montos, hist_conteos = self.get_dual_historical_data(day_limit)
        
        # 2. Traer mes actual
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(amount), COUNT(id) FROM "Clients_expense"
                WHERE merchant_id = %s AND anio = %s AND mes = %s
                AND EXTRACT(DAY FROM date) <= %s
            """, [self.merchant_id, self.hoy.year, self.hoy.month, day_limit])

            curr_monto, curr_conteo = cursor.fetchone()
            curr_monto = float(curr_monto or 0)
            curr_conteo = float(curr_conteo or 0)

        z_monto = self.calculate_z_score(curr_monto, hist_montos) if hist_montos else None
        z_frecuencia = self.calculate_z_score(curr_conteo, hist_conteos) if hist_conteos else None

         # Sin datos suficientes en alguno → no evaluamos
        if z_monto is None or z_frecuencia is None:
          return None
        
        avg_frecuencia = round(float(np.mean(hist_conteos)), 2) if hist_conteos else 0
        avg_monto = round(float(np.mean(hist_montos)), 2) if hist_montos else 0

        return {
            "merchant_id": self.merchant_id,
            "name": self.clean_name,
            "usuario": self.usuario,
            "monto_actual": curr_monto,
            "avg_monto": avg_monto,
            "frecuencia_actual": curr_conteo,
            "avg_frecuencia": avg_frecuencia,
            "z_monto": z_monto,
            "z_frecuencia": z_frecuencia,
            "alerta": z_monto > 3.0 or z_frecuencia > 3.0
            # alerta es un flag que se activa si alguno de los Z-Scores supera 2.0, indicando una posible anomalía
        }
    
    def calculate_z_score(self, current, history):
        if len(history) < 3: # Mínimo 3 meses para que la estadística sea seria
            return None
        
        # mean y std esperan una lista de valores float

        mean = np.mean(history).round(2)
        std = np.std(history).round(2)
        
        if std == 0: return 0.0
        return float((current - mean) / std)

    def analizar_gastos(self, day_limit = int):
    # 1. Obtenemos los IDs de todos los merchants que tienen al menos un gasto
    # Esto evita procesar merchants vacíos
        ids_activos = Merchant.objects.all()
    
        alertas_activas = []

        for m_id in ids_activos:
        # Cambiamos el ID de la instancia actual para evaluar al siguiente
         self.merchant_id = m_id.id
         self.clean_name = m_id.clean_name
         self.usuario = m_id.usuario

         analisis = self.evaluate_merchant(day_limit)        
         if analisis['alerta']:
            alertas_activas.append(analisis)

    
        return alertas_activas 

    def analizar_gastos_unico(self, day_limit= int):    
        alertas_activas = []

        analisis = self.evaluate_merchant(day_limit)    

         # AGREGAR ESTA GUARDA:
        if analisis is None:
         return alertas_activas  # retorna lista vacía, no explota

        if analisis['alerta']:
            alertas_activas.append(analisis)

    
        return alertas_activas 
    
