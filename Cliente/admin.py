from django.contrib import admin
from .models import Customer, Cotizador

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('names', 'dni', 'email', 'phone', 'movil', 'created')
    search_fields = ('names', 'dni', 'email')
    ordering = ('names',)

@admin.register(Cotizador)
class CotizadorAdmin(admin.ModelAdmin):
    list_display = ('customer', 'tipo_poliza', 'vigencia', 'vencimiento', 'total')
    list_filter = ('tipo_poliza', 'vigencia')
    fields = (
        'customer', 'vigencia', 'plazo', 'vencimiento', 'tipo_poliza',
        'valor_asegurado', 'tasa', 'prima_minima', 'prima', 'derecho', 'iva', 'total'
    )
    readonly_fields = ('prima_minima', 'prima', 'derecho', 'iva', 'total')