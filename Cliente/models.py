from django.db import models
from decimal import Decimal

# Create your models here.
class Customer(models.Model):
    names = models.CharField(max_length=150, verbose_name="Nombres")
    dni = models.CharField(max_length=13, verbose_name="RUC o Cédula")
    email = models.EmailField(max_length=150, verbose_name="Correo Electrónico")
    address = models.TextField(verbose_name="Dirección")
    phone = models.CharField(max_length=15, verbose_name="Teléfono")
    movil = models.CharField(max_length=15, verbose_name="Celular")
    avatar = models.ImageField(upload_to="avatar", verbose_name="Foto del Cliente", null=True, blank=True)
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de Creación")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Modificación")

    def __str__(self):
        return self.names

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "customer"
        ordering = ['id']



# Modelo de Cotizador
class Cotizador(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Cliente")
    vigencia = models.DateField(verbose_name="Vigencia")
    plazo = models.PositiveIntegerField(verbose_name="Plazo (días)")
    vencimiento = models.DateField(verbose_name="Vencimiento")
    tipo_poliza = models.CharField(
        max_length=50,
        verbose_name="Tipo de Póliza",
        choices=[
            ('BUEN USO DEL ANTICIPO', 'Buen Uso del Anticipo'),
            ('OTRO TIPO', 'Otro Tipo'),
        ]
    )
    valor_asegurado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Asegurado")
    tasa = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Tasa (%)")
    prima_minima = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prima Mínima", blank=True, null=True)
    prima = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prima", blank=True, null=True)
    derecho = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Derecho", default=3.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IVA", blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total", blank=True, null=True)
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de Creación")

    def save(self, *args, **kwargs):
        # Cálculos automáticos
        print(f"valor_asegurado: {self.valor_asegurado} ({type(self.valor_asegurado)})")
        print(f"tasa: {self.tasa} ({type(self.tasa)})")
        print(f"derecho: {self.derecho} ({type(self.derecho)})")
        self.prima = (Decimal(self.valor_asegurado) * Decimal(self.tasa)) / Decimal('100')
        self.prima_minima = max(self.prima, Decimal('50'))  # Ejemplo: la prima mínima debe ser $50
        self.iva = (Decimal(self.prima) + Decimal(self.derecho)) * Decimal('0.15')
        self.total = Decimal(self.prima) + Decimal(self.derecho) + Decimal(self.iva)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.names} - {self.tipo_poliza} - {self.total}"

    class Meta:
        verbose_name = "Cotizador"
        verbose_name_plural = "Cotizadores"
        db_table = "cotizador"
        ordering = ['id']
