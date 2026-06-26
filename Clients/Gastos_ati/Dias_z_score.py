from Clients.Gastos_ati.BaseZScoreAnalyzer import BaseZScoreAnalyzer

Base = BaseZScoreAnalyzer()

def Quincenal(cierre_mes= False):
   dia_corte = 30 if cierre_mes else 15

   resultados = Base.analizar_gastos(dia_corte)
   
   return {
        "resultados": resultados
    }

def Acumulado(day_limit= int):
   day = day_limit 
   resultados = Base.analizar_gastos(day)
   
   return resultados

def Acumulado_Unique(day_limit= int):
   day = day_limit 
   resultados = Base.analizar_gastos_unico(day)
   
   return resultados
