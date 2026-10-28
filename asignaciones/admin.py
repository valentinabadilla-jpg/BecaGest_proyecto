
from django.contrib import admin
from .models import Asignacion


@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'evaluacion',
        'monto_mensual',
        'fecha_asignacion',
        'estado'
    ]

    list_filter = ['estado', 'fecha_asignacion']

    search_fields = ['id']
