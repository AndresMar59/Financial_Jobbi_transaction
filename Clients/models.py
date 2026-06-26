from django.db import models

class Merchant(models.Model):
    brex_id = models.CharField(max_length=255, unique=True)
    raw_name = models.CharField(max_length=255) # El primero que llegó
    clean_name = models.CharField(max_length=255) # El nombre procesado para ML normalizado
    category_group = models.CharField(max_length=50)
    internal_category = models.CharField(max_length=50) # Tu categoría normalizada
    usuario = models.CharField(max_length=255, null=True, blank=True) # Para asignar manualmente si es necesario


class Expense(models.Model):
    brex_id_unico = models.CharField(max_length=255, unique=True, blank=True) # ID único de la transacción en Brex
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    date = models.DateTimeField()
    anio = models.IntegerField(max_length=4) # Numero
    mes = models.IntegerField(max_length=2)  # Numero
    location = models.CharField(max_length=255, null=True, blank=True)
    adress = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    mcc = models.CharField(max_length=10, null=True, blank=True)


