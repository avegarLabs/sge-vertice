from django.db import models

from rechum.models import BaseUrls
from adm.models import Departamento, UnidadOrg


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
    descripcion_ot = models.CharField(max_length=100, null=False, blank=False)
    no_contrato = models.CharField(max_length=5, null=False, blank=False, unique=True)
    valor_contrato = models.DecimalField(max_digits=9, decimal_places=2, editable=False, default=0.00)
    tipo_servicio = models. ForeignKey(Servicio, on_delete=models.DO_NOTHING, default='')
    area = models.ForeignKey(Area, on_delete=models.DO_NOTHING, default='')
    inversionista = models.ForeignKey(Inversionista, on_delete=models.DO_NOTHING, default='')
    OPT_Unidad = (('03', 'USTI'), ('07', 'UGDD'))
    unidad = models.CharField(max_length=4, choices=OPT_Unidad, default='', null=False, blank=False)

    def __str__(self):
        return '{} {}'.format(self.codigo_ot, self.descripcion_ot)


class TipoActividad(BaseUrls, models.Model):
    nombre_tipo_act = models.CharField(max_length=60, blank=False, null=False, unique=True, verbose_name='Nombre')
    valor = models.PositiveIntegerField(unique=True, verbose_name='Código')

    def __str__(self):
        return '{}'.format(self.nombre_tipo_act)

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


class Surtido(BaseUrls, models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre)

class TipoServicio(BaseUrls, models.Model):
    nombre = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre)

class TipoObra(BaseUrls, models.Model):
    nombre = models.CharField(max_length=60, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre)

class Programa(BaseUrls, models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre)

class Rol(BaseUrls, models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.nombre)

class Etapa(BaseUrls, models.Model):
    nombre = models.CharField(max_length=160, blank=False, null=False)
    codigo = models.CharField(max_length=20, blank=False, null=False)
    inicio_rango = models.DateField()
    fin_rango = models.DateField()
    clasificador_etapa = models.CharField(max_length=20, blank=False, null=False)
    surtido = models.CharField(max_length=100, blank=False, null=False)
    seguimiento = models.CharField(max_length=60, blank=False, null=False)
    anticipo = models.CharField(max_length=160, blank=False, null=False)
    vista = models.CharField(max_length=50, blank=False, null=False)


class Clientes(BaseUrls, models.Model):
    nombre = models.CharField(max_length=160, blank=False, null=False)
    codigo_reup = models.CharField(verbose_name='Código Reup',max_length=20, blank=False, null=False)
    codigo_compartido = models.CharField(verbose_name='Código Compartido', max_length=20, blank=False, null=False)
    organismo = models.CharField(verbose_name='Organismo', max_length=100, blank=False, null=False)
    resolucion_const = models.CharField(verbose_name='Resolución Constitucion', max_length=60, blank=False, null=False)
    direccion = models.CharField(verbose_name='Dirección', max_length=160, blank=False, null=False)
    telefono = models.CharField(verbose_name='Teléfono', max_length=50, blank=False, null=False)
    fax = models.CharField(max_length=50, blank=False, null=False)
    nit = models.CharField(max_length=20, blank=False, null=False)
    acronimo = models.CharField(verbose_name='Acrónimo', max_length=20, blank=False, null=False)
    grupo_empresarial = models.CharField(verbose_name='Grupo Empresarial', max_length=60, blank=False, null=False)
    fecha = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return '{}'.format(self.nombre)

class Banco(BaseUrls, models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)
    denominacion = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return '{} - {}'.format(self.nombre, self.codigo)

class Moneda(BaseUrls, models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    simbolo = models.CharField(max_length=10, blank=False, null=False)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.simbolo)

class CuentaBancaria(BaseUrls, models.Model):
    empresa = models.ForeignKey(Clientes, on_delete=models.DO_NOTHING)
    moneda = models.ForeignKey(Moneda, on_delete=models.DO_NOTHING)
    banco = models.ForeignKey(Banco, on_delete=models.DO_NOTHING)
    cuenta_bancaria = models.CharField(max_length=100, blank=False, null=False)
    numero_cuenta = models.CharField(max_length=100, blank=False, null=False)
    licencia = models.CharField(max_length=100, blank=False, null=False)
    registro_comercio = models.CharField(max_length=100, blank=False, null=False)


class SolicitudServicio(BaseUrls, models.Model):
    consecutivo = models.CharField(max_length=10, blank=False, null=False)
    fecha_recepcion = models.DateField()
    servicio = models.CharField(max_length=100, blank=False, null=False)
    etapa = models.ForeignKey(Etapa, on_delete=models.DO_NOTHING)
    cliente = models.ForeignKey(Clientes, on_delete=models.DO_NOTHING)
    unidad_org = models.ForeignKey(UnidadOrg, on_delete=models.DO_NOTHING)
    lleva_oferta = models.BooleanField(editable=True, default=False)
    para_contrato = models.BooleanField(editable=True, default=False)
    representado_por = models.CharField(max_length=100, blank=True, null=True)
    representado_por_cargo = models.CharField(max_length=100, blank=True, null=True)
    segun_resolucion = models.CharField(max_length=100, blank=True, null=True)
    segun_acuerdo = models.CharField(max_length=100, blank=True, null=True)
    nombre_firma_contrato = models.CharField(verbose_name='Nombre y apellidos del que firmará el Contrato', max_length=100, blank=True, null=True)
    cargo_firma_contrato = models.CharField(verbose_name='Cargo del que firmará', max_length=100, blank=True, null=True)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.DO_NOTHING)
    tipo_obras = models.ForeignKey(TipoObra, on_delete=models.DO_NOTHING)
    servicio_ingenieria = models.CharField(max_length=100, blank=False, null=False)
    otros = models.CharField(verbose_name='Otros', max_length=100, blank=False, null=False)
    otros1 = models.CharField(verbose_name='Otros', max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=100, blank=False, null=False)
    area_estudio = models.BooleanField(editable=False, default=False)
    resp_organos_consulta = models.BooleanField(editable=False, default=False)
    certif_micro = models.BooleanField(editable=False, default=False)
    tarea_proyeccion = models.BooleanField(editable=False, default=False)
    tarea_tecnica = models.BooleanField(editable=False, default=False)
    info_digital = models.BooleanField(editable=False, default=False)
    planos = models.BooleanField(editable=False, default=False)
    licencia_construccion = models.BooleanField(editable=False, default=False)
    licencia_ambiental = models.BooleanField(editable=False, default=False)
    est_ing_ecologico = models.BooleanField(editable=False, default=False)
    otros_documentos = models.CharField(max_length=100, blank=False, null=False)
    estado = models.CharField(max_length=100, blank=False, null=False)
    aprobado_por = models.CharField(max_length=100, blank=False, null=False)
    orden_trabajo = models.CharField(max_length=100, blank=False, null=False)
    observaciones = models.CharField(max_length=100, blank=False, null=False)
    num_contrato = models.CharField(max_length=100, blank=False, null=False)
    fecha_aprobacion = models.DateField()
    fecha_paralizacion = models.DateField()
    fecha_reanudacion = models.DateField()
    fecha_rechazo = models.DateField()
    fecha_cancelacion = models.DateField()


class Ofertas(BaseUrls, models.Model):
    solicitud_servicio = models.ForeignKey(SolicitudServicio, on_delete=models.DO_NOTHING)
    fecha_entrega_prep_tec = models.DateField()
    fecha_terminacion = models.DateField()
    fecha_entregada = models.DateField()
    fecha_aprobacion = models.DateField()
    estado = models.CharField(max_length=100, blank=False, null=False)
    observaciones = models.CharField(max_length=100, blank=False, null=False)


class Proyectos(BaseUrls, models.Model):
    solicitud_servicio = models.ForeignKey(SolicitudServicio, on_delete=models.DO_NOTHING)
    programa = models.ForeignKey(Programa, on_delete=models.DO_NOTHING)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    nombre_abreviado = models.CharField(max_length=100, blank=False, null=False)
    cliente = models.ForeignKey(Clientes, on_delete=models.DO_NOTHING)
    inicio_prep_tec = models.DateField()
    descripcion = models.CharField(max_length=100, blank=False, null=False)
    fecha_inicial_est = models.DateField()
    fecha_inicio_real = models.DateField()
    fecha_inicial_ajust = models.DateField()
    inicio_alcance_actual = models.DateField()
    duracion = models.CharField(max_length=100, blank=False, null=False)
    duracion_ajustada = models.CharField(max_length=100, blank=False, null=False)
    duracion_alcance_actual = models.CharField(max_length=100, blank=False, null=False)
    fecha_final_est = models.DateField()
    fecha_final_real = models.DateField()
    fecha_fin_ajustada = models.DateField()
    fin_alcance_actual = models.DateField()
    cant_miembros = models.CharField(max_length=100, blank=False, null=False)
    cant_planos = models.CharField(max_length=100, blank=False, null=False)

class Contratos(BaseUrls, models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    solicitud_servicio = models.ForeignKey(SolicitudServicio, on_delete=models.DO_NOTHING)
    orden_trabajo = models.CharField(max_length=100, blank=False, null=False)
    fecha_entrega_prep_tec = models.DateField()
    fecha_terminacion = models.DateField()
    fecha_entregada = models.DateField()
    fecha_aprobacion = models.DateField()
    estado = models.CharField(max_length=100, blank=False, null=False)
    observaciones = models.CharField(max_length=100, blank=False, null=False)

class Suplementos(BaseUrls, models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.DO_NOTHING)
    solicitud_servicio = models.ForeignKey(SolicitudServicio, on_delete=models.DO_NOTHING)
    orden_trabajo = models.CharField(max_length=100, blank=False, null=False)
    fecha_entrega_prep_tec = models.DateField()
    fecha_terminacion = models.DateField()
    fecha_entregada = models.DateField()
    fecha_aprobacion = models.DateField()
    estado = models.CharField(max_length=100, blank=False, null=False)
    observaciones = models.CharField(max_length=100, blank=False, null=False)