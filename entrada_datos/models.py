from django.db import models

from rechum.models import BaseUrls
from adm.models import Departamento


class Inversionista(BaseUrls, models.Model):
    codigo_inv = models.CharField(max_length=12, blank=False, null=False, unique=True)
    nombre_inv = models.CharField(max_length=60, blank=False, null=False)
    direccion_inv = models.CharField(max_length=160, blank=False, null=False)
    municipio_sucursal_inv = models.CharField(max_length=20, blank=False, null=False)
    sucursal_mn_inv = models.CharField(max_length=60, blank=False, null=False)
    cuenta_mn_inv = models.CharField(max_length=16, blank=False, null=False, unique=True)
    sucursal_usd_inv = models.CharField(max_length=16, blank=False, null=False)
    cuenta_usd_inv = models.CharField(max_length=16, blank=False, null=False, unique=True)
    nit = models.CharField(max_length=11, blank=False, null=False, unique=True)

    def __str__(self):
        return '{} {}'.format(self.codigo_inv, self.nombre_inv)


class Area (BaseUrls, models.Model):
    codigo = models.PositiveIntegerField(null=False, blank=False, verbose_name='Código')
    area = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False, blank=False)
    nombre = models.CharField(max_length=20, null=False, unique=True, blank=False)

    def __str__(self):
        return '{}'.format(self.nombre)


class Servicio (BaseUrls, models.Model):
    codigo = models.CharField(null=False, blank=False, unique=True, max_length=2, verbose_name='Código')
    nombre = models.CharField(max_length=20, null=False, unique=True, blank=False)

    def __str__(self):
        return '{}'.format(self.nombre)


class OT(BaseUrls, models.Model):
    codigo_ot = models.CharField(max_length=10, unique=True)
    descripcion_ot = models.CharField(verbose_name='Descripción del Servicio', max_length=100, null=False, blank=False)
    alcance = models.CharField(verbose_name='Alcance', max_length=200, null=False, blank=False)
    no_contrato = models.CharField(max_length=5, null=False, blank=False, unique=True)
    valor_contrato = models.DecimalField(max_digits=9, decimal_places=2, null=False, default=0.00)
    tipo_servicio = models. ForeignKey(Servicio, on_delete=models.DO_NOTHING, default='')
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, default='')
    inversionista = models.ForeignKey(Inversionista, on_delete=models.DO_NOTHING, default='')
    OPT_Unidad = (('03', 'USTI'), ('07', 'UGDD'))
    unidad = models.CharField(max_length=4, choices=OPT_Unidad, default='', null=False, blank=False)
    fecha_recepcion = models.DateField(verbose_name='Fecha de Recepción de Solicitud', null=True, blank=True)
    fecha_aprobacion = models.DateField(verbose_name='Fecha de Aprobación de Solicitud', null=True, blank=True)
    fecha_entrega_pt = models.DateField(verbose_name='Fecha de Entrega de la PT', null=True, blank=True)
    fecha_terminado_contrato = models.DateField(verbose_name='Fecha de Terminado Contrato', null=True, blank=True)
    fecha_entrega_cliente = models.DateField(verbose_name='Fecha Entrega al Cliente', null=True, blank=True)
    fecha_firma_contrato = models.DateField(verbose_name='Fecha de Firma del Contrato', null=True, blank=True)
    fecha_recepcion_contrato = models.DateField(verbose_name='Fecha de Recepción del Contrato', null=True, blank=True)


    def __str__(self):
        return '{} {}'.format(self.codigo_ot, self.descripcion_ot)


class TipoActividad(BaseUrls, models.Model):
    nombre_tipo_act = models.CharField(max_length=60, blank=False, null=False, unique=True, verbose_name='Nombre')
    valor = models.PositiveIntegerField(unique=True, verbose_name='Código')

    def __str__(self):
        return '{} {}'.format(self.valor, self.nombre_tipo_act)

    class Meta:
        verbose_name = 'Tipo de Actividad'
        verbose_name_plural = 'Tipos de Actividades'


class Actividad(BaseUrls, models.Model):
    tipo_act = models.ForeignKey(TipoActividad, on_delete=models.DO_NOTHING, default='', null=False, blank=False)
    codigo_act = models.PositiveIntegerField(null=False, verbose_name='Código', blank=False)
    descripcion_act = models.CharField(max_length=100, null=False, blank=True)
    valor_prod_act = models.DecimalField(max_digits=9, decimal_places=2, editable=False, default=0.00)
    activa = models.BooleanField(editable=False, default=True)
    orden_trab = models.ForeignKey(OT, on_delete=models.DO_NOTHING, verbose_name='Orden de Trabajo', default='', null=False, blank=False)
    numero = models.PositiveIntegerField(null=False, blank=False, verbose_name='Número', default=1)
    valor_act = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Valor', default=0.00)
    prod_tecleada = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Producción Tecleada', default=0.00)
    venta = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return '{} {}'.format(self.codigo_act, self.descripcion_act)

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

class UnidadFacturacion(BaseUrls, models.Model):
    codigo_uf = models.CharField(max_length=12, blank=False, null=False)
    nombre_uf = models.CharField(max_length=60, blank=False, null=False)
    direccion_uf = models.CharField(max_length=160, blank=False, null=False)
    municipio_sucursal = models.CharField(max_length=10, blank=False, null=False)
    sucursal_mn = models.CharField(max_length=60, blank=False, null=False)
    cuenta_mn = models.CharField(max_length=16, blank=False, null=False)
    sucursal_usd = models.CharField(max_length=16, blank=False, null=False)
    cuenta_usd = models.CharField(max_length=16, blank=False, null=False)
    nit = models.CharField(max_length=11, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre_uf)


class Suplemento(BaseUrls, models.Model):
    orden_trab = models.ForeignKey(OT, on_delete=models.DO_NOTHING)
    monto = models.DecimalField(max_digits=7, decimal_places=2)
    fecha = models.DateField()
    usuario = models.CharField(max_length=100)
    solicitud = models.CharField(max_length=60)
