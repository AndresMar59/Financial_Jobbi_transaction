from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse # <-- Añade esta importación

# Una función de vista rápida en el mismo archivo
def health_check(request):
    return HttpResponse("OK", content_type="text/plain")

urlpatterns = [
    path('health/', health_check), # <-- Añade esta línea para la raíz "/"
    path('admin/', admin.site.urls),
    path('api/webhooks/', include('webhooks.urls')),
]












