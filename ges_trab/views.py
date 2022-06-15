import decimal
import json
from datetime import datetime, date
from decimal import Decimal

from django.contrib.auth.decorators import permission_required
from django.db import IntegrityError
from django.db.models import F, Sum, Count
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from plantilla.models import Cargo, Plantilla
from rechum.utils import generate_pisa_report
from rechum.views import SgeListView, SgeCreateView, SgeDetailView, SgeUpdateView, SgeDeleteView, TemplateView
from adm.models import EscalaSalarial, Especialidad, EscalaSalarialReforma
from .filters import TrabajadorFilter
from .forms import *
from .models import *

check = False

MOTIVOS_BAJA = [
    {"key": '01', "value": 'Rescisión del contrato a voluntad del trabajador'},
    {"key": '02', "value": 'Motivos salariales'},
    {"key": '03', "value": 'Deficiente organización del trabajo'},
    {"key": '04', "value": 'Lejanía del centro de trabajo'},
    {"key": '05', "value": 'Inconveniencia del horario de trabajo'},
    {"key": '06', "value": 'No trabajar dentro de la especialidad'},
    {"key": '07', "value": 'Condiciones anormales de trabajo'},
    {"key": '08', "value": 'Escasa posibilidad de superación'},
    {"key": '09', "value": 'Problemas de vivienda y o ausencia de servicios sociales'},
    {"key": '10', "value": 'Inconformidad con los métodos de dirección'},
    {"key": '11', "value": 'Matrimonio atención a menores y familiares'},
    {"key": '12', "value": 'Bajas de trabajadores por sanción laboral'},
    {
        "key": '13',
        "value":
            'Bajas por no reincorporarse después de cumplido el período de vacaciones o licencia no retribuida'
    },
    {"key": '14', "value": 'Bajas por salida del país'},
    {"key": '15', "value": 'Bajas por Jubilación'},
    {"key": '16', "value": 'Bajas por Fallecimiento'},
    {"key": '17', "value": 'Otras bajas por fluctuación'}
]



class TrabListView(SgeListView):
    permission_required = 'ges_trab.read_trabajador'
    model = Trabajador
    template_name = 'trabajador/list.html'
    raise_exception = True
    queryset = Trabajador.objects.filter(fecha_baja__isnull=True).order_by('unidad_org_id', 'departamento_id', 'org_plantilla')

    def get_context_data(self, *, object_list=None, trabajador_filter=None, **kwargs):
        queryset = self.get_queryset()
        object_list = queryset.annotate(
        unidad_nombre=F('unidad_org__nombre'),
        dpto_nombre=F('departamento__nombre'),
        dpto_codigo=F('departamento__codigo'),
        cargo_nombre=F('cargo__nombre'),
        grupo_escala=F('escala_salarial_ref__grupo')).order_by('dpto_codigo', 'org_plantilla', '-grupo_escala')
        trabajador_filter = TrabajadorFilter(self.request.GET, queryset=object_list)
        return super().get_context_data(object_list=object_list, trabajador_filter=trabajador_filter, **kwargs)


class TrabCreateView(SgeCreateView):
    permission_required = 'ges_trab.add_trabajador'
    model = Trabajador
    form_class = TrabajadorForm
    template_name = 'trabajador/create.html'
    success_url = reverse_lazy('trabajador_create')


class TrabDetailView(SgeDetailView):
    permission_required = 'ges_trab.read_trabajador'
    model = Trabajador
    template_name = 'trabajador/detail.html'


class TrabUpdateView(SgeUpdateView):
    permission_required = 'ges_trab.change_trabajador'
    model = Trabajador
    form_class = TrabajadorForm
    template_name = 'trabajador/create.html'
    success_url = reverse_lazy('trabajador_list')


class TrabDeleteView(SgeDeleteView):
    permission_required = 'ges_trab.delete_trabajador'
    model = Trabajador
    success_url = reverse_lazy('trabajador_list')


class ReportsView(TemplateView):
    template_name = 'reports/trabajadores.html'

class TrabMenu(TemplateView):
    template_name = 'trabajador/worker_models_template.html'

class BajaListView(SgeListView):
    model = BajaOther
    template_name = 'bajas/list.html'
    permission_required = 'ges_trab.read_trabajador'

    def get_context_data(self, *, object_list=None, **kwargs):
        object_list = self.model.objects.annotate(
            especialidad_nombre=F('especialidad__nombre')
        ).order_by('fecha_baja')
        return super().get_context_data(object_list=object_list, **kwargs)


class BajaCreateView(SgeCreateView):
    model = BajaOther
    template_name = 'bajas/create.html'
    permission_required = 'ges_trab.add_trabajador'
    fields = '__all__'


class BajaDetailView(SgeDetailView):
    model = BajaOther
    template_name = 'bajas/detail.html'
    permission_required = 'ges_trab.read_trabajador'


@permission_required('ges_trab.read_movimiento', login_url='home_principal')
def listar_movimiento(request):
    list_movimiento = Movimiento.objects.all()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    fecha_inicio_convert = ''
    fecha_fin_convert = ''
    if fecha_inicio:
        fecha_inicio_convert = datetime.strptime(fecha_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
    if fecha_fin:
        fecha_fin_convert = datetime.strptime(fecha_fin, '%d/%m/%Y').strftime('%Y-%m-%d')

    if fecha_inicio and fecha_fin:
        list_movimiento = Movimiento.objects.filter(fecha__range=[fecha_inicio_convert, fecha_fin_convert])

    elif not fecha_fin and fecha_inicio:
        list_movimiento = Movimiento.objects.filter(fecha__gte=fecha_inicio_convert)
    elif fecha_fin and not fecha_inicio:
        list_movimiento = Movimiento.objects.filter(fecha__lte=fecha_fin_convert)
    else:
        list_movimiento = Movimiento.objects.all()
    return render(request, 'Listar_Movimiento.html', {'list_movimiento': list_movimiento})


@permission_required('ges_trab', login_url='home_principal')
def listar_disponible(request):
    list_disponible = Disponible.objects.all()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:

        fecha_inicio_convert = datetime.strptime(fecha_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
        fecha_fin_convert = datetime.strptime(fecha_fin, '%d/%m/%Y').strftime('%Y-%m-%d')
        list_disponible = Disponible.objects.filter(fecha__range=[fecha_inicio_convert, fecha_fin_convert])

    elif not fecha_fin and fecha_inicio:

        fecha_inicio_convert = datetime.strptime(fecha_inicio, '%d/%m/%Y').strftime('%Y-%m-%d')
        list_disponible = Disponible.objects.filter(fecha__range=[fecha_inicio_convert, '2200-01-01'])
    elif fecha_fin and not fecha_inicio:
        fecha_fin_convert = datetime.strptime(fecha_fin, '%d/%m/%Y').strftime('%Y-%m-%d')
        list_disponible = Disponible.objects.filter(fecha__range=['1970-01-01', fecha_fin_convert])
    else:
        list_disponible = Disponible.objects.all()

    return render(request, 'Listar_Disponibilidad.html', {'list_disponible': list_disponible})


@permission_required(('ges_trab.read_cpl', 'ges_trab.add_cpl'), login_url='home_principal')
def gestionar_cpl(request):
    list_cpl = Cpl.objects.all()
    context = {'list_cpl': list_cpl}
    return render(request, 'Gestionar_cpl.html', context)


@permission_required('ges_trab.read_nucleofamiliar', login_url='home_principal')
def gestionar_nucleo_familiar(request):
    list_nucleo_fam = NucleoFamiliar.objects.all()
    context = {'list_nucleo_fam': list_nucleo_fam}
    return render(request, 'Gestionar_Nucleo_Familiar.html', context)


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def gestionar_trabajador(request):
    list_trabajador = Trabajador.objects.filter(fecha_baja__isnull=True).select_related("unidad_org").select_related(
        "departamento").select_related("cargo").select_related("escala_salarial").select_related(
        "actividad").select_related("calificacion").select_related("especialidad").order_by("departamento__codigo", "org_plantilla")
    trabajador_filter = TrabajadorFilter(request.GET, queryset=list_trabajador)

    return render(request, 'Gestionar_Trabajador.html', {'trabajador_filter': trabajador_filter})


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def informaciones_trabajador(request):
    list_trabajador = Trabajador.objects.filter(fecha_baja__isnull=True).select_related("unidad_org").select_related(
        "departamento").select_related("cargo").select_related("escala_salarial").select_related(
        "actividad").select_related("calificacion").select_related("especialidad").order_by("departamento__codigo", "org_plantilla")
    trabajador_filter = TrabajadorFilter(request.GET, queryset=list_trabajador)

    return render(request, 'Informaciones_Trabajador.html', {'trabajador_filter': trabajador_filter})


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def gestionar_bajatrabajador(request):
    list_baja = Trabajador.objects.filter(fecha_baja__isnull=False)
    motivos_baja = {
        "01": 'Rescisión del contrato a voluntad del trabajador',
        "02": 'Motivos salariales',
        "03": 'Deficiente organización del trabajo',
        "04": 'Lejanía del centro de trabajo',
        "05": 'Inconveniencia del horario de trabajo',
        "06": 'No trabajar dentro de la especialidad',
        "07": 'Condiciones anormales de trabajo',
        "08": 'Escasa posibilidad de superación',
        "09": 'Problemas de vivienda y o ausencia de servicios sociales',
        "10": 'Inconformidad con los métodos de dirección',
        "11": 'Matrimonio atención a menores y familiares',
        "12": 'Bajas de trabajadores por sanción laboral',
        "13": 'Bajas por no reincorporarse después de cumplido el período de vacaciones o licencia no retribuida',
        "14": 'Bajas por salida del país',
        "15": 'Bajas por Jubilación',
        "16": 'Bajas por Fallecimiento',
        "17": 'Otras bajas por fluctuación'
    }
    return render(request, 'Gestionar_Baja.html', {'list_baja': list_baja, 'motivos': motivos_baja})


@permission_required('ges_trab.add_trabajador', login_url='home_principal')
def adicionar_trabajador_inline(request, trabajador_id=None):
   
    CODIGO_RESOLUCION_19 = '01'
    CODIGO_RESOLUCION_53 = '02'
    
    import datetime as dt_base
    globals()['check'] = False
    if trabajador_id:
        globals()['check'] = True
        trabajador = Trabajador.objects.get(pk=trabajador_id)
        cargo_id2 = trabajador.cargo_id
        departamento_id2 = trabajador.departamento_id
        cargo_bd = trabajador.cargo.nombre
        departamento_bd = trabajador.departamento.nombre
        salario_total_bd = trabajador.salario_total_reforma
        sal_plus_bd = trabajador.sal_plus
        salario_escala_bd = trabajador.salario_escala_ref
        sal_cat_cient_bd = trabajador.sal_cat_cient
        escala_salarial_bd = trabajador.escala_salarial_ref
        categoria_bd = trabajador.categoria
    else:
        trabajador = Trabajador()
        trabajador.escala_salarial_id = 1
    NucleoFamiliarFormSet = inlineformset_factory(
        Trabajador, NucleoFamiliar, fields=(
            'parentesco', 'fecha_nac', 'enfermedades', 'salario_dev', 'vinc_lab'
        ), form=NucleoFamiliarForm, extra=3, can_delete=True)
    if request.method == 'POST':
        inline = NucleoFamiliarFormSet(request.POST, instance=trabajador)  # , prefix='inline'
        form = TrabajadorForm(request.POST, request.FILES, instance=trabajador)

        if form.is_valid() and inline.is_valid():
            # Esto es para el rango de edad
            ci = form.cleaned_data['ci']
            semi_year = int(ci[0: 2])
            if 45 < semi_year < 99:
                fecha_nacimiento = '19' + ci[0: 2] + '-' + ci[2: 4] + '-' + ci[4: 6]
            else:
                fecha_nacimiento = '20' + ci[0: 2] + '-' + ci[2: 4] + '-' + ci[4: 6]
            trabajador.fecha_nac = fecha_nacimiento
            # Esto es para decrementar la disponibilidad de un cargo
            if not check:
                cargo_id = (form.cleaned_data['cargo'])
                departamento_id = (form.cleaned_data['departamento'])
                plantilla = Plantilla.objects.filter(cargo_id=cargo_id, departamento_id=departamento_id).get()
                plantilla.disponibles = plantilla.disponibles - 1
                plantilla.save()
            # Esto es para el salario por categoria cientifica
            if form.cleaned_data['cat_cient'] == '2':
                trabajador.sal_cat_cient = 440
            elif form.cleaned_data['cat_cient'] == '3':
                trabajador.sal_cat_cient = 825
            else:
                trabajador.sal_cat_cient = 0
            # Esto es para el salario total
            salario_escala = (form.cleaned_data['salario_escala_ref'])
          
            sal_plus = (form.cleaned_data['sal_plus'])
            sal_cond_anor = (form.cleaned_data['sal_cond_anor'])
            j_laboral = (form.cleaned_data['j_laboral'])
            escala_salarial = (form.cleaned_data['escala_salarial_ref'])
            categoria = (form.cleaned_data['categoria'])
            if not j_laboral:
                s_escala = 0.00
                if trabajador.resolucion == CODIGO_RESOLUCION_19:
                    s_escala = trabajador.escala_salarial_ref.salario_escala
                elif trabajador.resolucion == CODIGO_RESOLUCION_53:                    
                    s_escala = trabajador.escala_salarial_ref.salario_escala_53
                    
                trabajador.salario_escala_ref = s_escala
                trabajador.salario_total_reforma = s_escala + sal_plus + trabajador.sal_cat_cient
            else:
                trabajador_salario_jornada_laboral = (salario_escala / Decimal(190.60)) * 208
                trabajador.salario_jornada_laboral = round(trabajador_salario_jornada_laboral, 2)

                salario_total = ((salario_escala / Decimal(
                    190.60)) * 208) + sal_plus + trabajador.sal_cat_cient
             
                trabajador.salario_total_reforma = round(salario_total, 2)
            # Esto es para registrar el movimiento
            if trabajador_id:
                departamento_form = form.cleaned_data['departamento'].nombre
                cargo_form = form.cleaned_data['cargo'].nombre
                departamento = form.cleaned_data['departamento']
                cargo = form.cleaned_data['cargo']
                if (departamento_form != departamento_bd) or (cargo_form != cargo_bd):
                    # Aumentar disponibilidad
                    plantilla2 = Plantilla.objects.filter(cargo_id=cargo_id2, departamento_id=departamento_id2).get()
                    plantilla2.disponibles = plantilla2.disponibles + 1

                    # Decrementar disponibilidad
                    plantilla = Plantilla.objects.filter(cargo_id=cargo, departamento_id=departamento).get()
                    plantilla.disponibles = plantilla.disponibles - 1

                    if plantilla.disponibles >= 0:
                        plantilla2.save()
                        plantilla.save()
                    # Movimiento
                    movimiento = Movimiento()
                    movimiento.trabajador_id = trabajador_id
                    movimiento.area_act = departamento
                    movimiento.area_ant = departamento_bd
                    movimiento.cargo_act = cargo
                    movimiento.cargo_ant = cargo_bd
                    movimiento.cies_ant = Decimal(0.00)
                    movimiento.cies_act = Decimal(0.00)
                    movimiento.antiguedad_ant = Decimal(0.00)
                    movimiento.antiguedad_act = Decimal(0.00)
                    movimiento.categoria_ant = categoria_bd
                    movimiento.categoria_act = categoria
                    movimiento.incre_res_act = Decimal(0.00)
                    movimiento.incre_res_ant = Decimal(0.00)
                    movimiento.salario_escala_ant = salario_escala_bd
                    movimiento.salario_escala_act = salario_escala
                    movimiento.escala_salarial_ant = escala_salarial_bd
                    movimiento.escala_salarial_act = escala_salarial
                    movimiento.salario_total_ant = salario_total_bd

                    movimiento.salario_total_act = trabajador.salario_total_reforma
                    movimiento.sal_plus_ant = sal_plus_bd
                    movimiento.sal_plus_act = sal_plus
                    movimiento.fecha = dt_base.datetime.today()
                    movimiento.save()
                    trabajador.escala_salarial_ref_id = escala_salarial
                    trabajador.salario_escala_ref = salario_escala
                    # trabajador.salario_total_reforma = trabajador.calcular_salario_total_reforma
                    # trabajador.salario_total = sal_total_old
                    # print(trabajador.salario_total)
            # Esto es si el contrato es disponible
            t_contrato = (form.cleaned_data['t_contrato'])
            if t_contrato == '8':
                disponible = Disponible()
                disponible.trabajador_id = trabajador.pk
                disponible.fecha = dt_base.datetime.today()
                disponible.save()
            trabajador.incre_res = Decimal(0.00)
            trabajador.sal_bas = Decimal(0.00)
            trabajador.cies = Decimal(0.00)
            if trabajador.escala_salarial_ref_id == 15 and trabajador.unidad_org_id == 2:
                trabajador.escala_salarial_id = 10
            elif trabajador.escala_salarial_ref_id == 16 and trabajador.unidad_org_id == 2:
                trabajador.escala_salarial_id = 11

            trabajador.fecha_baja = None
            trabajador.motivo_baja = None
            form.save()
            inline.save()
            if request.POST.get("guardar"):
                return redirect('trabajador_list')
            elif request.POST.get("guardaradicionar"):
                return HttpResponse('AdicionarTrabajador')
    else:
        inline = NucleoFamiliarFormSet(instance=trabajador)
        if trabajador_id is None:
            form = TrabajadorAltaForm(instance=trabajador)
        else:
            form = TrabajadorForm(instance=trabajador)
    return render(request, 'Adicionar_Trabajador_inline.html', {'inline': inline, 'form': form, 'pk': trabajador.id})


@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def bajaeliminar(request, pk):
    from datetime import datetime as asdf
    trabajador = Trabajador.objects.get(pk=pk)
    print(trabajador.nombre_completo)
    if request.method == 'GET':
        return render(
            request, 'Baja_Trabajador.html',
            {'trabajador': trabajador, 'motivos': MOTIVOS_BAJA}
        )
    else:
        causal = request.POST.get('causa', None)
        now_date_str = asdf.now().strftime('%d/%m/%Y')
        fecha_baja_str = request.POST.get('fecha_baja', now_date_str)
        fecha_baja = asdf.strptime(fecha_baja_str, '%d/%m/%Y')
        plantilla = Plantilla.objects.filter(cargo_id=trabajador.cargo_id,
                                             departamento_id=trabajador.departamento_id).get()
        # ------------------------
        trabajador.fecha_baja = fecha_baja
        trabajador.motivo_baja = causal
        trabajador.save()
        # Aumentar disponibilidad del cargo
        plantilla.disponibles = plantilla.disponibles + 1
        plantilla.save()
        return redirect('trabajador_list')

def dep_unidad(request, pk):
    departamentos = Departamento.objects.filter(unidad_id=pk).order_by('codigo')
    datos = [{'nombre': dep.nombre, 'id': dep.id} for dep in departamentos]
    response = [{"success": 1, "result": datos}]
    return HttpResponse(json.dumps(response), content_type='application/json')

def cargar_datos(request):
    import datetime as dt_base
    trabajadores_list_altas = Alta.objects.all()
    movimientos_list = MovimientoReforma.objects.all()
    if movimientos_list.count() is 0:
        for trab in trabajadores_list_altas:
            # Movimiento
            movimiento = MovimientoReforma()
            movimiento.trabajador_id = trab.pk
            movimiento.area_act = trab.departamento.nombre
            movimiento.area_ant = trab.departamento.nombre
            movimiento.cargo_act = trab.cargo.nombre
            movimiento.cargo_ant = trab.cargo.nombre
            movimiento.cies_ant = trab.cies
            movimiento.antiguedad_ant = trab.antiguedad
            movimiento.categoria_ant = trab.categoria
            movimiento.categoria_act = trab.categoria
            movimiento.incre_res_ant = trab.incre_res
            movimiento.sal_plus_ant = trab.sal_plus
            movimiento.sal_cat_cient_ant = trab.salario_cat_cient_old
            movimiento.sal_cat_cient_act = trab.salario_cat_cient
            movimiento.fecha = dt_base.datetime.today()
            movimiento.escala_salarial_ant = trab.escala_salarial
            if trab.j_laboral:
                movimiento.salario_escala_ant = trab.salario_jornada_laboral
            else:
                movimiento.salario_escala_ant = trab.salario_escala
            movimiento.salario_total_ant = trab.salario_total
            movimiento.escala_salarial_act = trab.grupo_escala_reforma
            movimiento.salario_escala_act = trab.calcular_salario_escala_reforma
            movimiento.salario_total_act = trab.calcular_salario_total_reforma
            movimiento.save()
    else:
        for movimiento in movimientos_list:
            trab = Trabajador.objects.get(pk=movimiento.trabajador_id)
            movimiento.area_act = trab.departamento.nombre
            movimiento.area_ant = trab.departamento.nombre
            movimiento.cargo_act = trab.cargo.nombre
            movimiento.cargo_ant = trab.cargo.nombre
            movimiento.cies_ant = trab.cies
            movimiento.antiguedad_ant = trab.antiguedad
            movimiento.categoria_ant = trab.categoria
            movimiento.categoria_act = trab.categoria
            movimiento.incre_res_ant = trab.incre_res
            movimiento.sal_plus_ant = trab.sal_plus
            movimiento.sal_cat_cient_ant = trab.salario_cat_cient_old
            movimiento.sal_cat_cient_act = trab.salario_cat_cient
            # movimiento.fecha = dt_base.datetime.today()
            movimiento.escala_salarial_ant = str(trab.escala_salarial)
            if trab.j_laboral:
                movimiento.salario_escala_ant = trab.salario_jornada_laboral
            else:
                movimiento.salario_escala_ant = trab.salario_escala
            movimiento.salario_total_ant = trab.salario_total
            movimiento.escala_salarial_act = trab.grupo_escala_reforma
            movimiento.salario_escala_act = trab.calcular_salario_escala_reforma
            movimiento.salario_total_act = trab.calcular_salario_total_reforma
            movimiento.save()
            trab.escala_salarial_ref_id = adm.EscalaSalarialReforma.objects.get(grupo=trab.grupo_escala_reforma).id
            trab.salario_escala_ref = movimiento.salario_escala_act
            trab.salario_total_reforma = movimiento.salario_total_act
            trab.save()

    return redirect('rechum_home')

def documentacion_reforma(request):
    unidad_org = UnidadOrg.objects.all()
    departamento = Departamento.objects.all()
    if request.method == 'GET':
        return render(
            request, 'Documentacion_Reforma.html',
            {'unidad_org': unidad_org, 'departamento': departamento}
        )

    unidad_org = request.POST.get('unidad', None)
    departamento = request.POST.get('departamento', None)
    tipo_doc = request.POST['tipo_documento']
    if departamento == '0':
        movimientos_list = MovimientoReforma.objects.filter(trabajador__unidad_org_id=unidad_org)

    else:
        movimientos_list = MovimientoReforma.objects.filter(trabajador__unidad_org_id=unidad_org, trabajador__departamento_id=departamento)
    directorrh = Trabajador.objects.filter(cargo_id=179).get()
    if tipo_doc == '1':
        registrado_por = Alta.objects.filter(cargo_id=27, departamento_id=10, org_plantilla=0).get()
        template_path = 'Movimiento_Nomina_Reforma.html'
        context = {'movimientos_list': movimientos_list,
                   'elaborado': request.user, 'director': directorrh,
                   'registrado_por': registrado_por,
                   'title': f'Movimiento de Nomina – Reforma Salarial'}
        return generate_pisa_report(context, template_path, context['title'])
    elif tipo_doc == '2':
        template_path = 'Suplemento_Contrato_Reforma.html'
        context = {'movimientos_list': movimientos_list,
                   'director': directorrh,
                   'title': f'Suplemento de Contrato – Reforma Salarial'}
        return generate_pisa_report(context, template_path, context['title'])
    return redirect('rechum_home')

def cambiar(request):
    trabajadores_list_altas = Trabajador.objects.all()
    for trab in trabajadores_list_altas:
        trabajador = Trabajador.objects.get(pk=trab.pk)
        trabajador.escala_salarial_ref_id = adm.EscalaSalarialReforma.objects.get(grupo=trab.grupo_escala_reforma).id
        trabajador.salario_escala_ref = trab.salario_escala_reforma
        trabajador.salario_total_reforma = trab.calcular_salario_total_reforma
        trabajador.save()

    return redirect('rechum_home')

def cambiar_one(request, pk):
    trabajador = Trabajador.objects.get(pk=pk)
    trabajador.escala_salarial_ref_id = adm.EscalaSalarialReforma.objects.get(grupo=trabajador.grupo_escala_reforma).id
    trabajador.salario_escala_ref = trabajador.salario_escala_reforma
    trabajador.salario_total_reforma = trabajador.calcular_salario_total_reforma
    trabajador.save()
    return

@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_movimiento_nomina_reforma(request):
    movimientos_list = MovimientoReforma.objects.all()
    directorrh = Alta.objects.filter(cargo_id=179).get()
    registrado_por = Alta.objects.filter(cargo_id=27, departamento_id=10, org_plantilla=0).get()
    template_path = 'Movimiento_Nomina_Reforma.html'
    context = {'movimientos_list': movimientos_list,
               'elaborado': request.user, 'director': directorrh,
               'registrado_por': registrado_por,
               'title': f'Movimiento de Nomina – Reforma Salarial'}
    return generate_pisa_report(context, template_path, context['title'])

@permission_required('ges_trab.change_movimiento', login_url='home_principal')
def editar_movimiento(request, pk):
    import datetime as dt_base
    movimiento = Movimiento.objects.get(pk=pk)

    if request.method == 'POST':
        fecham = request.POST.get('fecha_movimiento')
        fechamov = dt_base.datetime.strptime(fecham, '%d/%m/%Y').strftime('%Y-%m-%d')
        select = request.POST.get('select', '')
        resolucion = request.POST.get('resolucion', '')
        tipom = resolucion + ' ' + select
        movimiento.fecha = fechamov
        movimiento.tipo = tipom
        movimiento.save()
        return redirect('ListarMovimiento')
    return render(request, 'Editar_Movimiento.html', {'movimiento': movimiento})


@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def editar_baja(request, pk):
    import datetime as dt_module
    baja = Trabajador.objects.filter(fecha_baja__isnull=False).get(pk=pk)

    if request.method == 'POST':
        fechab = request.POST.get('fecha_baja')
        motivo_baja = request.POST.get('causa_baja')
        fechabaj = dt_module.datetime.strptime(fechab, '%d/%m/%Y').strftime('%Y-%m-%d')

        baja.fecha_baja = fechabaj
        baja.motivo_baja = motivo_baja

        baja.save()
        return redirect('GestionarBaja')
    return render(request, 'Editar_Baja.html', {'baja': baja, 'motivos': MOTIVOS_BAJA})


@permission_required('ges_trab.delete_nucleofamiliar', login_url='home_principal')
def eliminar_familiar(request, pk):
    nucleof = NucleoFamiliar.objects.filter(pk=pk)
    nucleof.delete()


@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def daralta(request, pk):
    baja = Trabajador.objects.filter(fecha_baja__isnull=False).get(pk=pk)
    if request.method == 'GET':
        form = TrabajadorAltaBajaForm(instance=baja)
        return render(request, 'Alta_Trabajador.html', {'baja': form, 'pk': pk})
    elif request.method == 'POST':
        form = TrabajadorAltaBajaForm(request.POST)
        if form.is_valid():
            baja.update(form.cleaned_data)
            baja.update(fecha_baja=None)
            # todo verificar plantilla
            return redirect('GestionarBaja')
        return render(request, 'Alta_Trabajador.html', {'baja': form, 'pk': pk})
    else:
        return redirect('GestionarBaja')


###
# Ajax queries
###
@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def salarioescala_por_escalasarial(request, pk):
    escalasalarialref = EscalaSalarialReforma.objects.filter(pk=pk).get()   
    salario_escala = escalasalarialref.salario_escala_53
    
    datos = [{'salario_escala_ref': str(salario_escala),
              'id': escalasalarialref.id}]
    response = [{"success": 1, "result": datos}]
    return HttpResponse(json.dumps(response), content_type='application/json')

@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def salarioescala_por_resolucion(request, pk, codigo_resolucion):   
    CODIGO_RESOLUCION_19 = '01'
    CODIGO_RESOLUCION_53 = '02'
    
    escalasalarialref = EscalaSalarialReforma.objects.filter(pk=pk).get() 
    salario_escala = 0.00
    if codigo_resolucion == CODIGO_RESOLUCION_53:  
        salario_escala = escalasalarialref.salario_escala_53
    elif codigo_resolucion == CODIGO_RESOLUCION_19:
        salario_escala = escalasalarialref.salario_escala
    
    datos = [
        {'salario_escala_ref': str(salario_escala),
        'id': escalasalarialref.id}
    ]
    
    response = [{"success": 1, "result": datos}]
    return HttpResponse(json.dumps(response), content_type='application/json')

@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def cargos_disponibles(request, departamento_id):
    cargos = Cargo.objects.filter(plantilla__departamento_id=departamento_id).annotate(
        plantilla_disp=Sum('plantilla__disponibles')).exclude(plantilla_disp=0).values('id', 'nombre')
    response = [{"success": 1, "result": list(cargos)}]
    return HttpResponse(json.dumps(response), content_type='application/json')

def cargo_por_dpto(request, pk):
    # cargos = Cargo.objects.filter(departamento=pk).values('id', 'nombre').order_by('codigo')
    cargos = Cargo.objects.filter(plantilla__departamento_id=pk).annotate(
        plantilla_disp=Sum('plantilla__disponibles')).exclude(plantilla_disp=0).values('id', 'nombre')
    response = [{"success": 1, "result": list(cargos)}]
    return HttpResponse(json.dumps(response), content_type='application/json')

def trabajador_por_ci(request, ci):
    try:     
        trabajador = Trabajador.objects.get(ci=ci)
        id = trabajador.id 
        success = 1
    except:
        id = 0
        success = 0   
    response = [{"success": success, "result": id}]
    return HttpResponse(json.dumps(response), content_type='application/json')


@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def calificacion_especialidad(request, calificacion_id):
    especialidades = list(Especialidad.objects.filter(calificacion_id=calificacion_id).values('id', 'nombre'))
    response = [{"success": 1, "result": especialidades}]
    return HttpResponse(json.dumps(response), content_type='application/json')


@permission_required('ges_trab.change_trabajador', login_url='home_principal')
def check_codigo(request, pk=0):
    is_available = "false"
    if check is True:
        return HttpResponse("true")
    if request.is_ajax():
        codigo_interno = request.GET.get("codigo_interno")  # Change post to get
        try:
            Alta.objects.exclude(id=pk).get(codigo_interno=codigo_interno)
        except ObjectDoesNotExist:
            is_available = "true"
    return HttpResponse(is_available)


@permission_required('ges_trab.change_trabajador', raise_exception=True)
def check_usuario(request, pk=None):
    is_available = "false"
    if check is True:
        return HttpResponse("true")
    if request.is_ajax():
        usuario = request.GET.get("usuario")  # Change post to get
        if usuario == 'Ninguno':
            return HttpResponse("true")
        try:
            Alta.objects.exclude(id=pk).get(usuario=usuario)
        except ObjectDoesNotExist:
            is_available = "true"
    return HttpResponse(is_available)


@permission_required('ges_trab.change_trabajador', raise_exception=True)
def check_ci(request, pk=None):
    is_available = "false"
    if check is True:
        return HttpResponse("true")
    if request.is_ajax():
        ci = request.GET.get("ci")  # Change post to get
        try:
            Alta.objects.exclude(id=pk).get(ci=ci)
        except ObjectDoesNotExist:
            is_available = "true"
    return HttpResponse(is_available)


@permission_required(('ges_trab.change_trabajador', 'ges_trab.change_movimiento'), raise_exception=True)
def check_plantilla(request):
    is_available = "false"
    if check is True:
        return HttpResponse("true")
    if request.is_ajax():
        org_plantilla = request.GET.get("org_plantilla")  # Change post to get
        try:
            Alta.objects.get(org_plantilla=org_plantilla)
        except ObjectDoesNotExist:
            is_available = "true"
    return HttpResponse(is_available)


###
# Web view reports
###

REPORTS = {
    # 1: 'Listado por departamentos',
    2: 'Distribución por áreas',
    3: 'Distribución por género',
    7: 'Distribución por etnia',
    4: 'Distribución por rango edades',
    5: 'Carreras por departamentos',
    6: 'Cargos por departamentos',
    8: 'Total por áreas'
}


def _listado_x_departamento(model, year=None, month=None, from_date=None, to_date=None):
    queryset = model.objects.annotate(
        unidad_nombre=F('unidad_org__nombre'),
        departamento_nombre=F('departamento__nombre'),
        especialidad_nombre=F('especialidad__nombre'),
        cargo_nombre=F('cargo__nombre')
    ).order_by('unidad_org_id', 'departamento_id')
    context = {'tipo_reporte': REPORTS, 'reporte_id': 1}
    if from_date:
        queryset = queryset.filter(fecha_contrato__range=[from_date, to_date])
        context.update({'from_date': from_date, 'to_date': to_date})
    elif year:
        queryset = queryset.filter(fecha_contrato__year=year)
        context.update({'date': date(year, 1, 1), 'year': year})
        if month:
            queryset = queryset.filter(fecha_contrato__month=month)
            context.update({'date': date(year, month, 1), 'month': month})
    else:
        current_year = date.today().year
        queryset = queryset.filter(fecha_contrato__year=current_year)
        context.update({'date': date(current_year, 1, 1), 'year': current_year})
    context['object_list'] = queryset
    return context


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def altas_x_departamento(request, year=None, month=None, from_date=None, to_date=None):
    context = _listado_x_departamento(Alta, year, month, from_date, to_date)
    context['alta_baja'] = True
    return render(request, 'reports/trabajador/altas_x_departamento.html', context)


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def bajas_x_departamento(request, year=None, month=None, from_date=None, to_date=None):
    context = _listado_x_departamento(BajaOther, year, month, from_date, to_date)
    context['alta_baja'] = False
    return render(request, 'reports/trabajador/bajas_x_departamento.html', context)


@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_x_departamento(request):
    return render(request, 'reports/trabajador/layout_chart.html', {
        "tipo_reporte": REPORTS, 'reporte_id': 2, 'chart_url': 'dist-bar-drilldown'
    })


@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_altas_x_genero(request):
    return render(request, 'reports/trabajador/layout_chart.html', {
        "tipo_reporte": REPORTS, 'reporte_id': 3, 'alta_baja': True, 'chart_url': 'gender-pie-alta'
    })


@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_bajas_x_genero(request):
    return render(request, 'reports/trabajador/layout_chart.html', {
        "tipo_reporte": REPORTS, 'reporte_id': 3, 'alta_baja': False, 'chart_url': 'gender-pie-baja'
    })


@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_altas_x_etnia(request):
    return render(request, 'reports/trabajador/layout_chart.html', {
        'tipo_reporte': REPORTS, 'reporte_id': 7, 'alta_baja': True, 'chart_url': 'etnia-pie-alta'
    })


@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_bajas_x_etnia(request):
    return render(request, 'reports/trabajador/layout_chart.html', {
        'tipo_reporte': REPORTS, 'reporte_id': 7, 'alta_baja': False, 'chart_url': 'etnia-pie-baja'
    })


# todo add age average
@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_altas_x_rango_edades(request):
    return render(request, 'reports/trabajador/dist_x_rango_edades.html', {
        "tipo_reporte": REPORTS, 'reporte_id': 4, 'alta_baja': True, 'chart_url': 'age-pyramid-alta'
    })


@permission_required('ges_trab.report_trabajador', raise_exception=True)
def dist_bajas_x_rango_edades(request):
    return render(request, 'reports/trabajador/dist_x_rango_edades.html', {
        "tipo_reporte": REPORTS, 'reporte_id': 4, 'alta_baja': False, 'chart_url': 'age-pyramid-baja'
    })


@permission_required('adm.report_especialidad', raise_exception=True)
def dist_esp_x_dep(request):
    univ = request.POST.get('univ', None)
    get_by = request.POST.get('get_by', 'dep')
    context = _request_esp_x_dep(univ, get_by)
    context.update({'tipo_reporte': REPORTS, 'reporte_id': 5, 'univ': univ, 'get_by': get_by})
    return render(request, 'reports/trabajador/dist_esp_x_dept.html', context)


@permission_required('adm.report_cargo', raise_exception=True)
def dist_cargos_x_dep(request):
    univ = request.POST.get('univ', None)
    get_by = request.POST.get('get_by', 'dep')
    context = _request_cargos_x_dep(univ, get_by)
    context.update({'tipo_reporte': REPORTS, 'reporte_id': 6, 'univ': univ, 'get_by': get_by})
    return render(request, 'reports/trabajador/dist_cargos_x_dept.html', context)


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def total_x_areas(request):
    context = {}
    return render(request, 'reports/trabajador/total_x_area.html', context)


###
# Reports pdf
###
@permission_required('ges_trab.export_trabajador', raise_exception=True)
def exportar(request, pk):
    trabajador = Alta.objects.get(pk=pk)
    template_path = 'Contrato_Pdf.html'
    context = {'trabajador': trabajador, "title": "Contrato de Trabajo"}
    return generate_pisa_report(context, template_path, f"{context['title']} – {trabajador.nombre_completo}")


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def exportar_acuerdo(request, pk):
    trabajador = Alta.objects.get(pk=pk)
    template_path = 'Acuerdo_Confidencialidad.html'
    context = {'trabajador': trabajador, 'title': 'Acuerdo de Confidencialidad'}
    return generate_pisa_report(context, template_path, f"{context['title']} – {trabajador.nombre_completo}")


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def exportar_solic_cuenta_user(request, pk):
    trabajador = Alta.objects.get(pk=pk)
    template_path = 'Solicitud_Cuenta_Usuario.html'
    context = {'trabajador': trabajador, 'title': 'Solicitud de Cuenta de Usuario'}
    return generate_pisa_report(context, template_path, f"{context['title']} – {trabajador.nombre_completo}")

class MovimientoListView(SgeListView):
    permission_required = 'plantilla.read_movimiento'
    raise_exception = True
    model = Movimiento
    template_name = 'movimiento/list.html'

class MovimientoCreateView(SgeCreateView):
    pass


class MovimientoUpdateView(SgeUpdateView):
    pass


class MovimientoDetailView(SgeDetailView):
    pass


class MovimientoDeleteView(SgeDeleteView):
    pass


@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_movimiento_nomina(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    directorrh = Alta.objects.filter(cargo_id=179).get()
    registrado_por = Alta.objects.filter(cargo_id=29, departamento_id=10, org_plantilla=0).get()
    template_path = 'Movimiento_Nomina.html'
    context = {'trabajador': movimiento.trabajador, 'movimiento': movimiento,
               'elaborado': request.user, 'director': directorrh,
               'dia': movimiento.fecha.day, 'mes': movimiento.fecha.month,
               'anno': movimiento.fecha.year, 'registrado_por': registrado_por,
               'title': f'Movimiento de Nomina – {movimiento.trabajador.nombre_completo}'}
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_movimiento_nomina_alta(request, pk):
    trabajador = Alta.objects.get(pk=pk)
    directorrh = Alta.objects.filter(cargo_id=179).get()
    registrado_por = Alta.objects.filter(cargo_id=29, departamento_id=10, org_plantilla=0).get()
    template_path = 'Movimiento_Nomina_Alta.html'
    context = {'trabajador': trabajador, 'elaborado': request.user,
               'director': directorrh, 'dia': trabajador.fecha_alta.day,
               'mes': trabajador.fecha_alta.month, 'anno': trabajador.fecha_alta.year,
               'title': f'Movimiento de Nomina – Alta {trabajador.nombre_completo}',
               'registrado_por': registrado_por}
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_movimiento_nomina_baja(request, pk):
    trabajador = BajaOther.objects.get(pk=pk)
    directorrh = Alta.objects.filter(cargo_id=179).get()
    registrado_por = Alta.objects.filter(cargo_id=27, departamento_id=10).get()
    template_path = 'Movimiento_Nomina_Baja.html'
    context = {'trabajador': trabajador, 'elaborado': request.user,
               'director': directorrh, 'dia': trabajador.fecha_baja.day,
               'mes': trabajador.fecha_baja.month, 'anno': trabajador.fecha_baja.year,
               'registrado_por': registrado_por,
               'title': f'Movimiento Nomina Baja – {trabajador.nombre_completo}'}
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def all_altas_report(request, year, month=None):
    context = _request_workers_year_month_delta(year, month=month, alta=True)
    template_path = 'reports/trabajador/export/altas_x_departamento.html'
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def all_bajas_report(request, year, month=None):
    context = _request_workers_year_month_delta(year, month=month)
    template_path = 'reports/trabajador/export/bajas_x_departamento.html'
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def exportar_altas(request):
    from_date = request.POST.get('fecha_inic', None)
    to_date = request.POST.get('fecha_fin', None)
    template_path = 'reports/trabajador/export/altas_x_departamento.html'
    context = _request_workers_date_delta(from_date, to_date, True)
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_trabajador', raise_exception=True)
def exportar_bajas(request):
    from_date = request.POST.get('fecha_inic', None)
    to_date = request.POST.get('fecha_fin', None)
    template_path = 'reports/trabajador/export/bajas_x_departamento.html'
    context = _request_workers_date_delta(from_date, to_date)
    return generate_pisa_report(context, template_path, context['title'])


@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_movimientos(request):
    fecha_inic = request.POST['fecha_inic']
    fecha_fin = request.POST['fecha_fin']
    template_path = 'Reporte_Movimientos_Altas_Bajas.html'
    context = _request_report_movimiento(fecha_inic, fecha_fin)
    return generate_pisa_report(context, template_path, "Movimientos Altas y Bajas")


@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_suplemento_contrato(request, pk):
    movimiento = Movimiento.objects.get(pk=pk)
    directorrh = Trabajador.objects.filter(cargo_id=179).get()
    template_path = 'Suplemento_Contrato.html'
    context = {'trabajador': movimiento.trabajador, 'movimiento': movimiento,
               'director': directorrh, 'dia': movimiento.fecha.day,
               'mes': movimiento.fecha.month, 'anno': movimiento.fecha.year,
               'title': f'Suplemento de Contrato – {movimiento.trabajador.nombre_completo}'}
    return generate_pisa_report(context, template_path, context['title'])


TITLE_BY = {
    'emp': 'en la Empresa',
    'uni': 'por Unidad Organizacional',
    'dep': 'por Departamento'
}


@permission_required('adm.export_especialidad', raise_exception=True)
def dist_esp_x_dep_report(request):
    univ = request.POST.get('univ', None)
    get_by = request.POST.get('get_by', 'dep')
    context = _request_esp_x_dep(univ, get_by)
    context['get_by'] = get_by
    context['title'] = f'Carreras {TITLE_BY[get_by]}'
    template_name = 'reports/trabajador/export/esp_x_departamento.html'
    return generate_pisa_report(context, template_name, context['title'])


@permission_required('adm.export_cargo', raise_exception=True)
def dist_cargo_x_dep_report(request):
    univ = request.POST.get('univ', None)
    get_by = request.POST.get('get_by', 'dep')
    context = _request_cargos_x_dep(univ, get_by)
    context['get_by'] = get_by
    context['title'] = f'Cargos y Carreras {TITLE_BY[get_by]}'
    template_name = 'reports/trabajador/export/cargos_x_departamento.html'
    return generate_pisa_report(context, template_name, context['title'])


# @permission_required('ges_trab.export_trabajador', raise_exception=True)
def export_ubicacion_en_defensa(request):
    defensa = Trabajador.objects.filter(fecha_baja__isnull=True).values('orga_defensa').distinct().annotate(
        count=Count('orga_defensa')
    ).values('orga_defensa', 'count')
    objects_list = []
    total = Alta.objects.all().count()
    for element in defensa:
        cant = Trabajador.objects.filter(orga_defensa=element['orga_defensa'], fecha_baja__isnull=True).count()
        porci = round(cant / total * 100, 2)
        objects_list.append(Defensa(nombre=element['orga_defensa'], cantidad=cant, porciento=porci))
    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)

    template_name = 'reports/defensa/resumen_situacion_defensa.html'
    context = {
        'object_list': objects_list,
        'total': total,
        'title': 'Situacion en la Defensa',
        'fecha_creacion': fecha,
        'dia': dia
    }
    return generate_pisa_report(context, template_name, context['title'])


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def preview_resumen_plantilla(request):
    context = _request_resumen_plantilla()
    context['title'] = "Resumen de Plantilla"
    template_name = 'reports/resumen_plantilla_preview.html'
    context['export_pdf'] = 'resumen-plantilla_report'
    return render(request, template_name, context)

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def export_resumen_plantilla(request):
    # if rep == 1:
    #     context = _request_total_etnia()
    #     context['title'] = "Resumen de Plantilla"
    #     template_name = 'reports/resumen_plantilla.html'
    # else:
    context = _request_resumen_plantilla()
    context['title'] = "Resumen de Plantilla"
    template_name = 'reports/resumen_plantilla.html'

    return generate_pisa_report(context, template_name, context['title'])


def _request_resumen_plantilla():
    queryset = Trabajador.objects.filter(fecha_baja__isnull=True).values('t_contrato').distinct().annotate(
        count=Count('t_contrato')).values('t_contrato', 'count')
    total = Alta.objects.all().count()
    objects_list = []
    total_a = 0
    total_c = 0
    total_o = 0
    total_s = 0
    total_t = 0
    for element in queryset:
        if element['t_contrato'] == '1':
            nombre = 'Nombramiento'
        elif element['t_contrato'] == '2':
            nombre = 'Indeterminado'
        elif element['t_contrato'] == '3':
            nombre = 'Determinado por tiempo definido '
        elif element['t_contrato'] == '7':
            nombre = 'Determinado por sustitución de trabajador'
        elif element['t_contrato'] == '4':
            nombre = 'Adiestramiento'
        elif element['t_contrato'] == '5':
            nombre = 'Disponible'
        elif element['t_contrato'] == '6':
            nombre = 'A Prueba'
        id = element['t_contrato']
        cant_masc = Alta.objects.filter(sexo='M', t_contrato=id).count()
        cant_fem = Alta.objects.filter(sexo='F',t_contrato=id).count()
        cant_fem_c = Alta.objects.filter(sexo='F', categoria='C', t_contrato=id).count()
        cant_fem_a = Alta.objects.filter(sexo='F', categoria='A', t_contrato=id).count()
        cant_fem_s = Alta.objects.filter(sexo='F', categoria='S', t_contrato=id).count()
        cant_fem_o = Alta.objects.filter(sexo='F', categoria='O', t_contrato=id).count()
        cant_fem_t = Alta.objects.filter(sexo='F', categoria='T', t_contrato=id).count()
        cant_masc_c = Alta.objects.filter(sexo='M', categoria='C', t_contrato=id).count()
        cant_masc_a = Alta.objects.filter(sexo='M', categoria='A', t_contrato=id).count()
        cant_masc_s = Alta.objects.filter(sexo='M', categoria='S', t_contrato=id).count()
        cant_masc_o = Alta.objects.filter(sexo='M', categoria='O', t_contrato=id).count()
        cant_masc_t = Alta.objects.filter(sexo='M', categoria='T', t_contrato=id).count()
        objects_list.append(Cantidades(nombre=nombre, cant_masc=cant_masc, cant_fem=cant_fem,
                                       cant_fem_c=cant_fem_c, cant_fem_a=cant_fem_a, cant_fem_s=cant_fem_s,
                                       cant_fem_o=cant_fem_o, cant_fem_t=cant_fem_t, cant_masc_c=cant_masc_c,
                                       cant_masc_a=cant_masc_a, cant_masc_s=cant_masc_s, cant_masc_t=cant_masc_t,
                                       cant_masc_o=cant_masc_o, id=id))

    objects_list = list(objects_list)
    for item in objects_list:
        total_a += item.cant_masc_a + item.cant_fem_a
        total_c += item.cant_masc_c + item.cant_fem_c
        total_o += item.cant_masc_o + item.cant_fem_o
        total_s += item.cant_masc_s + item.cant_fem_s
        total_t += item.cant_masc_t + item.cant_fem_t
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)

    return {"object_list": objects_list, "total": total, "total_a": total_a, "total_c": total_c, "total_o": total_o,
            "total_s": total_s, "total_t": total_t, 'fecha_creacion': fecha, 'dia': dia}


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def registro_defensa(request, org_defensa=None):
    context = _request_registro_defensa()
    context['title'] = 'Registro Militar'
    template_name = 'reports/defensa/registro_militar.html'
    return generate_pisa_report(context, template_name, context['title'])

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def asignado_a_defensa(request):
    context = _request_registro_defensa()
    context['title'] = "Defensa"
    template_name = 'reports/defensa/ubicacion_en_defensa.html'
    return generate_pisa_report(context, template_name, context['title'])

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def choferes_en_defensa(request):
    context = _request_registro_defensa(True)
    context['title'] = "Ubicacion en la defensa de los Choferes"
    template_name = 'reports/defensa/choferes_en_la_defensa.html'
    return generate_pisa_report(context, template_name, context['title'])

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def trabajadores_x_contrato(request):
    context = _request_trabajadores_x_contrato()
    template_name = 'reports/trabajador/export/trabajadores_x_contrato.html'
    return generate_pisa_report(context, template_name, context['title'])


###
# Utility functions
###

def _request_workers_year_month_delta(year, month=None, alta=False):
    queryset = Trabajador.objects.filter(fecha_baja__isnull=alta).order_by('unidad_org_id', 'departamento_id', 'org_plantilla')
    str_out = year
    if month:
        str_out = date(year, month, 1).strftime('%m, %Y')
    title = f"Reporte {'Altas' if alta else 'Bajas'} {str_out}"
    if alta:
        queryset = queryset.filter(fecha_contrato__year=year)
        if month:
            queryset = queryset.filter(fecha_contrato__month=month)
    else:
        queryset = queryset.filter(fecha_baja__year=year)
        if month:
            queryset = queryset.filter(fecha_baja__month=month)
    queryset = queryset.annotate(
        unidad_nombre=F('unidad_org__nombre'),
        departamento_nombre=F('departamento__nombre'),
        cargo_nombre=F('cargo__nombre'),
        especialidad_nombre=F('especialidad__nombre')
    )
    return {'object_list': queryset, 'title': title}


def _request_report_movimiento(fecha_inic, fecha_fin):
    sql_alta = f"""
        SELECT
            ges_trab_trabajador.id, ges_trab_trabajador.primer_nombre, ges_trab_trabajador.segundo_nombre,
            ges_trab_trabajador.apellidos, ges_trab_trabajador.codigo_interno,
            ges_trab_trabajador.categoria, ges_trab_trabajador.departamento_id
        FROM public.ges_trab_trabajador
        WHERE
            ges_trab_trabajador.fecha_contrato BETWEEN '{fecha_inic}'::DATE AND '{fecha_fin}'::DATE
        ORDER BY
            ges_trab_trabajador.fecha_contrato ASC;
    """
    result1 = Trabajador.objects.raw(sql_alta)
    trabajadores_alta = []
    for element in result1:
        trabajadores_alta.append(element)

    sql_baja = f"""
        SELECT
            ges_trab_baja.id, ges_trab_baja.primer_nombre, ges_trab_baja.segundo_nombre,
            ges_trab_baja.apellidos, ges_trab_baja.codigo_interno, ges_trab_baja.departamento_id,
            ges_trab_baja.categoria
        FROM public.ges_trab_baja
        WHERE ges_trab_baja.fecha_baja BETWEEN '{fecha_inic}'::DATE AND '{fecha_fin}'::DATE
        ORDER BY ges_trab_baja.fecha_baja ASC;
    """
    result2 = Baja.objects.raw(sql_baja)
    trabajadores_baja = []
    for element in result2:
        trabajadores_baja.append(element)

    sql_mov = f"""
        SELECT ges_trab_movimiento.id, ges_trab_trabajador.primer_nombre, ges_trab_trabajador.segundo_nombre,
            ges_trab_trabajador.apellidos, ges_trab_trabajador.codigo_interno, ges_trab_movimiento.area_ant,
            ges_trab_trabajador.categoria,ges_trab_movimiento.area_act
        FROM public.ges_trab_movimiento, public.ges_trab_trabajador
        WHERE ges_trab_trabajador.id = ges_trab_movimiento.trabajador_id AND
            ges_trab_movimiento.fecha BETWEEN '{fecha_inic}'::DATE AND '{fecha_fin}'::DATE
        ORDER BY ges_trab_movimiento.fecha ASC;
    """
    result3 = Movimiento.objects.raw(sql_mov)
    trabajadores_mov = []
    for element in result3:
        trabajadores_mov.append(element)

    return {'trabajadores_alta': trabajadores_alta, 'trabajadores_baja': trabajadores_baja,
            'trabajadores_mov': trabajadores_mov, 'fecha_inic': fecha_inic, 'fecha_fin': fecha_fin}


def _request_workers_date_delta(fecha_inic, fecha_fin, alta=False):
    queryset = Trabajador.objects.filter(
        fecha_baja__isnull=alta)
    if alta:
        queryset = queryset.filter(
            fecha_contrato__range=[fecha_inic, fecha_fin]
        )
    else:
        queryset = queryset.filter(
            fecha_baja__range=[fecha_inic, fecha_fin]
        )
    queryset = queryset.annotate(
        unidad_nombre=F('unidad_org__nombre'),
        departamento_nombre=F('departamento__nombre'),
        cargo_nombre=F('cargo__nombre'),
        especialidad_nombre=F('especialidad__nombre')).order_by('unidad_org_id', 'departamento_id')
    title = f'Reporte {"Altas" if alta else "Bajas"} ({fecha_inic} a {fecha_fin})'

    return {'object_list': queryset, 'title': title}


def _request_esp_x_dep(univ=None, get_by=None):
    queryset = Alta.objects.filter(escolaridad='Univ') if univ else Alta.objects
    queryset = queryset.exclude(Q(especialidad_id__isnull=True)).values('especialidad_id').annotate(
        count=Count('especialidad_id'),
        esp_nombre=F('especialidad__nombre')
    )
    if get_by == 'emp':
        queryset = queryset.values(
            'esp_nombre', 'especialidad_id', 'count'
        ).order_by('-count', 'esp_nombre')
    elif get_by == 'uni':
        queryset = queryset.annotate(
            uni_nombre=F('unidad_org__nombre')
        ).values(
            'esp_nombre', 'unidad_org_id', 'especialidad_id', 'count', 'uni_nombre'
        ).order_by('unidad_org_id', '-count', 'esp_nombre')
    else:
        queryset = queryset.annotate(
            uni_nombre=F('unidad_org__nombre'),
            dep_nombre=F('departamento__nombre')
        ).values(
            'esp_nombre', 'unidad_org_id', 'departamento_id',
            'especialidad_id', 'count', 'uni_nombre', 'dep_nombre'
        ).order_by('unidad_org_id', 'departamento_id', '-count', 'esp_nombre')
    return {'object_list': queryset}


def _request_cargos_x_dep(univ=None, get_by=None):
    queryset = Alta.objects.filter(escolaridad='Univ') if univ else Alta.objects
    queryset = queryset.exclude(Q(especialidad_id__isnull=True)).values('cargo_id').annotate(
        cargo_nombre=F('cargo__nombre'),
        count=Count('cargo_id'),
        esp_nombre=F('especialidad__nombre')
    )
    if get_by == 'uni':
        queryset = queryset.annotate(
            uni_nombre=F('unidad_org__nombre')).values(
            'esp_nombre', 'unidad_org_id', 'cargo_nombre',
            'cargo_id', 'count', 'uni_nombre').order_by('unidad_org_id', '-count')
    elif get_by == 'emp':
        queryset = queryset.values(
            'esp_nombre', 'cargo_nombre',
            'cargo_id', 'count').order_by('-count')
    else:
        queryset = queryset.annotate(
            uni_nombre=F('unidad_org__nombre'),
            dep_nombre=F('departamento__nombre')).values(
            'esp_nombre', 'unidad_org_id', 'departamento_id', 'cargo_nombre',
            'cargo_id', 'count', 'uni_nombre', 'dep_nombre').order_by('unidad_org_id', 'departamento_id', '-count')
    return {'object_list': queryset}


def _request_registro_defensa(org_defensa=None):
    queryset = Alta.objects.exclude(orga_defensa__in=['FEI', 'Imp']).annotate(
        dep_nombre=F('departamento__nombre'),
        cargo_nombre=F('cargo__nombre')
    )
    if org_defensa:
        queryset = queryset.filter(cargo__nombre__startswith='Chofer').order_by('primer_nombre', 'segundo_nombre', 'apellidos')
    else:
        queryset = queryset.order_by('orga_defensa', 'primer_nombre', 'segundo_nombre', 'apellidos')
        queryset = sorted(queryset, key=lambda n: (
            0 if n.orga_defensa == 'U/R' else 1 if n.orga_defensa == 'MTT' else 2 if n.orga_defensa == 'BPD-LR ' else 3))
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {'fecha_creacion': fecha, 'dia': dia, "object_list": queryset, 'rename': {
        'U/R': 'Unidades Regulares',
        'BPD-LR': 'Brigada de Producción y Defensa en Lugar de Residencia',
        'BPD-PTG': 'Brigada de Producción y Defensa para Tiempo de Guerra',
        'MTT': 'Milicias de Tropas Territoriales'
    }}


@permission_required('ges_trab.export_movimiento', raise_exception=True)
def exportar_suplemento_contrato_reforma(request):
    movimientos_list = MovimientoReforma.objects.all()
    directorrh = Trabajador.objects.filter(cargo_id=179).get()
    template_path = 'Suplemento_Contrato_Reforma.html'
    context = {'movimientos_list': movimientos_list,
               'director': directorrh,
               'title': f'Suplemento de Contrato – Reforma Salarial'}
    return generate_pisa_report(context, template_path, context['title'])

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def escolaridad_categoria_preview(request):
    context = _request_escolaridad_categoria()
    context['title'] = "Totales por Escolaridad según Categoría Ocupacional"
    template_name = 'reports/escolaridad_categoria_preview.html'
    context['export_pdf'] = 'escolaridad-categoria_export'
    return render(request, template_name, context)


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def escolaridad_categoria_export(request):
    context = _request_escolaridad_categoria()
    context['title'] = "Totales por Escolaridad "
    template_name = 'reports/total_escolaridad_categoria.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_escolaridad_categoria():
    queryset = Trabajador.objects.filter(fecha_baja__isnull=True).values('escolaridad').distinct().annotate(
        count=Count('escolaridad')).values('escolaridad', 'count')
    total = Alta.objects.all().count()
    objects_list = []
    total_a = 0
    total_c = 0
    total_o = 0
    total_s = 0
    total_t = 0
    for element in queryset:
        nombre = element['escolaridad']
        id = 0
        cant_masc = Alta.objects.filter(sexo='M', escolaridad=nombre).count()
        cant_fem = Alta.objects.filter(sexo='F', escolaridad=nombre).count()
        cant_fem_c = Alta.objects.filter(sexo='F', categoria='C', escolaridad=nombre).count()
        cant_fem_a = Alta.objects.filter(sexo='F', categoria='A', escolaridad=nombre).count()
        cant_fem_s = Alta.objects.filter(sexo='F', categoria='S', escolaridad=nombre).count()
        cant_fem_o = Alta.objects.filter(sexo='F', categoria='O', escolaridad=nombre).count()
        cant_fem_t = Alta.objects.filter(sexo='F', categoria='T', escolaridad=nombre).count()
        cant_masc_c = Alta.objects.filter(sexo='M', categoria='C', escolaridad=nombre).count()
        cant_masc_a = Alta.objects.filter(sexo='M', categoria='A', escolaridad=nombre).count()
        cant_masc_s = Alta.objects.filter(sexo='M', categoria='S', escolaridad=nombre).count()
        cant_masc_o = Alta.objects.filter(sexo='M', categoria='O', escolaridad=nombre).count()
        cant_masc_t = Alta.objects.filter(sexo='M', categoria='T', escolaridad=nombre).count()
        objects_list.append(Cantidades(nombre=nombre, cant_masc=cant_masc, cant_fem=cant_fem,
                                       cant_fem_c=cant_fem_c, cant_fem_a=cant_fem_a, cant_fem_s=cant_fem_s,
                                       cant_fem_o=cant_fem_o, cant_fem_t=cant_fem_t, cant_masc_c=cant_masc_c,
                                       cant_masc_a=cant_masc_a, cant_masc_s=cant_masc_s, cant_masc_t=cant_masc_t,
                                       cant_masc_o=cant_masc_o, id=id))

    objects_list = list(objects_list)
    for item in objects_list:
        total_a += item.cant_masc_a + item.cant_fem_a
        total_c += item.cant_masc_c + item.cant_fem_c
        total_o += item.cant_masc_o + item.cant_fem_o
        total_s += item.cant_masc_s + item.cant_fem_s
        total_t += item.cant_masc_t + item.cant_fem_t

    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, "total": total, "total_a": total_a, "total_c": total_c, "total_o": total_o,
            "total_s": total_s, "total_t": total_t, 'fecha_creacion': fecha, 'dia': dia
            }


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def preview_total_etnia(request):
    context = _request_total_etnia()
    context['title'] = "Totales por Etnia según Categoría Ocupacional"
    template_name = 'reports/total_etnia_categoria_preview.html'
    context['export_pdf'] = 'total-etnia_report'
    return render(request, template_name, context)

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def export_total_etnia(request):
    context = _request_total_etnia()
    context['title'] = "Totales por Etnia"
    template_name = 'reports/total_etnia_categoria.html'
    return generate_pisa_report(context, template_name, context['title'])



def _request_total_etnia():
    queryset = Trabajador.objects.filter(fecha_baja__isnull=True).values('etnia').distinct().annotate(
        count=Count('etnia')).values('etnia', 'count')
    total = Alta.objects.all().count()
    objects_list = []
    total_a = 0
    total_c = 0
    total_o = 0
    total_s = 0
    total_t = 0
    for element in queryset:
        nombre = element['etnia']
        id = 0
        cant_masc = Alta.objects.filter(sexo='M', etnia=nombre).count()
        cant_fem = Alta.objects.filter(sexo='F', etnia=nombre).count()
        cant_fem_c = Alta.objects.filter(sexo='F', categoria='C', etnia=nombre).count()
        cant_fem_a = Alta.objects.filter(sexo='F', categoria='A', etnia=nombre).count()
        cant_fem_s = Alta.objects.filter(sexo='F', categoria='S', etnia=nombre).count()
        cant_fem_o = Alta.objects.filter(sexo='F', categoria='O', etnia=nombre).count()
        cant_fem_t = Alta.objects.filter(sexo='F', categoria='T', etnia=nombre).count()
        cant_masc_c = Alta.objects.filter(sexo='M', categoria='C', etnia=nombre).count()
        cant_masc_a = Alta.objects.filter(sexo='M', categoria='A', etnia=nombre).count()
        cant_masc_s = Alta.objects.filter(sexo='M', categoria='S', etnia=nombre).count()
        cant_masc_o = Alta.objects.filter(sexo='M', categoria='O', etnia=nombre).count()
        cant_masc_t = Alta.objects.filter(sexo='M', categoria='T', etnia=nombre).count()
        objects_list.append(Cantidades(nombre=nombre, cant_masc=cant_masc, cant_fem=cant_fem,
                                       cant_fem_c=cant_fem_c, cant_fem_a=cant_fem_a, cant_fem_s=cant_fem_s,
                                       cant_fem_o=cant_fem_o, cant_fem_t=cant_fem_t, cant_masc_c=cant_masc_c,
                                       cant_masc_a=cant_masc_a, cant_masc_s=cant_masc_s, cant_masc_t=cant_masc_t,
                                       cant_masc_o=cant_masc_o, id=id))

    objects_list = list(objects_list)
    for item in objects_list:
        total_a += item.cant_masc_a + item.cant_fem_a
        total_c += item.cant_masc_c + item.cant_fem_c
        total_o += item.cant_masc_o + item.cant_fem_o
        total_s += item.cant_masc_s + item.cant_fem_s
        total_t += item.cant_masc_t + item.cant_fem_t

    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, "total": total, "total_a": total_a, "total_c": total_c, "total_o": total_o,
            "total_s": total_s, "total_t": total_t, 'fecha_creacion': fecha, 'dia': dia
            }


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def total_areas_sexo(request):
    context = _request_total_areas_sexo()
    context['title'] = "Total por Areas y Sexo"
    template_name = 'reports/total_areas_sexo.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_total_areas_sexo():
    queryset = UnidadOrg.objects.all()
    objects_list = []
    elements = []
    for i in queryset:
        cant_fem = Trabajador.objects.filter(unidad_org_id=i.id, sexo='F', fecha_baja__isnull=True).count()
        cant_masc = Trabajador.objects.filter(unidad_org_id=i.id, sexo='M', fecha_baja__isnull=True).count()
        total = Trabajador.objects.filter(unidad_org_id=i.id, fecha_baja__isnull=True).count()
        dept = Departamento.objects.filter(unidad_id=i.id).values('nombre','codigo','id').order_by('codigo')
        for j in dept:
            descrip = j['nombre']
            subtotal = Trabajador.objects.filter(departamento_id=j['id'], fecha_baja__isnull=True).count()
            f = Trabajador.objects.filter(departamento_id=j['id'], sexo='F', fecha_baja__isnull=True).count()
            m = Trabajador.objects.filter(departamento_id=j['id'], sexo='M', fecha_baja__isnull=True).count()
            elements.append(Elements(nombre=descrip, total=subtotal, cant_fem=f, cant_masc=m))
        objects_list.append(ListPadre(nombre=i.nombre, elements=elements, cant_fem=cant_fem, cant_masc=cant_masc,
                                      total=total, iden=i.id))
        elements = []
    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, 'fecha_creacion': fecha, 'dia': dia}

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def total_especialidad_sexo(request):
    context = _request_total_especialidad_sexo()
    context['title'] = "Total por Especialidad y Sexo"
    template_name = 'reports/total_especialidad_sexo.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_total_especialidad_sexo():
    queryset1 = Trabajador.objects.filter(fecha_baja__isnull=True, calificacion_id__isnull=False).annotate(valor=F('calificacion__nombre')).values('calificacion', 'valor')
    queryset = queryset1.distinct('calificacion')
    objects_list = []
    elements = []
    for i in queryset:
        cant_fem = Trabajador.objects.filter(calificacion_id=i['calificacion'], sexo='F', fecha_baja__isnull=True).count()
        cant_masc = Trabajador.objects.filter(calificacion_id=i['calificacion'], sexo='M', fecha_baja__isnull=True).count()
        total = Trabajador.objects.filter(calificacion_id=i['calificacion'], fecha_baja__isnull=True).count()
        espec = Trabajador.objects.filter(calificacion_id=i['calificacion'], especialidad_id__isnull=False).distinct('especialidad').annotate(nombre=F('especialidad__nombre')).values('especialidad','nombre')
        for j in espec:
            descrip = j['nombre']
            subtotal = Trabajador.objects.filter(especialidad_id=j['especialidad'], fecha_baja__isnull=True).count()
            f = Trabajador.objects.filter(especialidad_id=j['especialidad'], sexo='F', fecha_baja__isnull=True).count()
            m = Trabajador.objects.filter(especialidad_id=j['especialidad'], sexo='M', fecha_baja__isnull=True).count()
            elements.append(Elements(nombre=descrip, total=subtotal, cant_fem=f, cant_masc=m))
        objects_list.append(ListPadre(nombre=i['valor'], elements=elements, cant_fem=cant_fem, cant_masc=cant_masc,
                                      total=total, iden=0))
        elements = []
    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, 'fecha_creacion': fecha, 'dia': dia}


def preview_trab_area_contrato_cat(request):
    context = _request_trab_area_contrato_cat()
    context['title'] = "Trabajadores por Contrato, Áreas y Categoría Ocupacional"
    template_name = 'reports/trab_area_contrato_cat_preview.html'
    context['export_pdf'] = 'trab_area_contrato_cat_report'
    return render(request, template_name, context)


def export_trab_area_contrato_cat(request):
    context = _request_trab_area_contrato_cat()
    context['title'] = "Trabajadores por Contrato "
    template_name = 'reports/trab_area_contrato_cat.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_trab_area_contrato_cat():
    queryset = Trabajador.objects.filter(fecha_baja__isnull=True).values('t_contrato').distinct().order_by('t_contrato')
    objects_list = []
    contr = ''
    for item in queryset:
        if item['t_contrato'] == '1':
            contr = 'Nombramiento'
        elif item['t_contrato'] == '2':
            contr = 'Indeterminado'
        elif item['t_contrato'] == '3':
            contr = 'Determinado por tiempo definido '
        elif item['t_contrato'] == '7':
            contr = 'Determinado por sustitución de trabajador'
        elif item['t_contrato'] == '4':
            contr = 'Adiestramiento'
        elif item['t_contrato'] == '5':
            contr = 'Disponible'
        elif item['t_contrato'] == '6':
            contr = 'A Prueba'
        id = item['t_contrato']
        personal = Trabajador.objects.filter(fecha_baja__isnull=True, t_contrato=id).values('codigo_interno', 'primer_nombre',
                                                                                            'segundo_nombre', 'apellidos', 'categoria').annotate( unidad=F('unidad_org__nombre'),
                                                                                                                                                  dpto=F('departamento__nombre'), cargo=F('cargo__nombre')).values('codigo_interno','primer_nombre',
                                                                                                                                                                                                                   'segundo_nombre', 'apellidos','unidad', 'dpto', 'cargo', 'categoria').order_by('unidad_org__id',
                                                                                                                                                                                                                                                                                                  'categoria')
        objects_list.append(Contrato(nombre=contr, no=id, personal=list(personal)))

    objects_list = list(objects_list)
    for j in objects_list:
        for k in j.personal:
            temp = UnidadOrg.objects.filter(nombre=k['unidad']).get().siglas
            k['unidad'] = temp
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, "fecha_creacion": fecha, 'dia': dia}


def cant_trab_edad_sexo_cat(request):
    context = _request_cant_trab_edad_sexo_cat()
    context['title'] = "Cantidad Trabaj por Edades"
    template_name = 'reports/cant_trab_edad_sexo_cat.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_cant_trab_edad_sexo_cat():
    queryset = UnidadOrg.objects.all()
    objects_list = []
    elements = []
    edades = []
    lis_edad = []

    for i in queryset:
        cant_feme = Alta.objects.filter(unidad_org_id=i.id, sexo='F').count()
        cant_mascu = Alta.objects.filter(unidad_org_id=i.id, sexo='M').count()
        total = Alta.objects.filter(unidad_org_id=i.id).count()
        lis_trab = Alta.objects.filter(unidad_org_id=i.id)
        temp = i.nombre
        for i in lis_trab:
            elements.append(List_Edades(nombre= i.nombre_completo, edad=i.age_by_ci, sexo=i.sexo, unidad=i.unidad_org_id,
                                        dpto=i.departamento_id, escolaridad=i.escolaridad,ci=i.ci, cargo=i.cargo,
                                        salario=i.salario_total_reforma, cat=i.categoria))
        elements = sorted(elements,key=lambda elements: elements.edad)
        for k in elements:
            edades.append(k.edad)
        edades1= sorted(set(edades))
        cant_masc = 0
        cant_fem = 0
        cant_fem_a = 0
        cant_fem_c = 0
        cant_fem_s = 0
        cant_fem_t = 0
        cant_fem_o = 0
        cant_masc_a = 0
        cant_masc_c = 0
        cant_masc_s = 0
        cant_masc_o = 0
        cant_masc_t = 0
        id = 0
        for e in edades1:
            nomb = e
            for h in elements:
                if h.edad == nomb:
                    id += 1
                    if h.sexo == 'M':
                        cant_masc+= 1
                    if h.sexo == 'F':
                        cant_fem+= 1
                    if h.sexo == 'F' and h.cat =='A':
                        cant_fem_a+= 1
                    if h.sexo == 'F' and h.cat =='C':
                        cant_fem_c+= 1
                    if h.sexo == 'F' and h.cat =='S':
                        cant_fem_s+= 1
                    if h.sexo == 'F' and h.cat =='O':
                        cant_fem_o+= 1
                    if h.sexo == 'F' and h.cat =='T':
                        cant_fem_t+= 1
                    if h.sexo == 'M' and h.cat == 'A':
                        cant_masc_a += 1
                    if h.sexo == 'M' and h.cat == 'C':
                        cant_masc_c += 1
                    if h.sexo == 'M' and h.cat == 'S':
                        cant_masc_s += 1
                    if h.sexo == 'M' and h.cat == 'O':
                        cant_masc_o += 1
                    if h.sexo == 'M' and h.cat == 'T':
                        cant_masc_t += 1
            lis_edad.append(Cantidades(nombre=nomb, cant_masc=cant_masc, cant_fem=cant_fem,cant_fem_c=cant_fem_c,
                                       cant_fem_a=cant_fem_a, cant_fem_s=cant_fem_s, cant_fem_o=cant_fem_o,
                                       cant_fem_t=cant_fem_t, cant_masc_c=cant_masc_c, cant_masc_a=cant_masc_a,
                                       cant_masc_s=cant_masc_s, cant_masc_o=cant_masc_o, cant_masc_t=cant_masc_t,id=id))
            cant_masc = 0
            cant_fem = 0
            cant_fem_a = 0
            cant_fem_c = 0
            cant_fem_s = 0
            cant_fem_t = 0
            cant_fem_o = 0
            cant_masc_a = 0
            cant_masc_c = 0
            cant_masc_s = 0
            cant_masc_o = 0
            cant_masc_t = 0
            id = 0

        objects_list.append(ListPadre(nombre=temp, elements=lis_edad, cant_fem=cant_feme, cant_masc=cant_mascu,
                                      total=total, iden=0))
        elements = []
        edades = []
        lis_edad = []

    suma_total = 0
    cal_promedio = Alta.objects.all()
    for prom in cal_promedio:
        suma_total += int(prom.age_by_ci[0:2])
    edad_promedio = Decimal(suma_total/cal_promedio.__len__()).quantize(Decimal('.01'))

    for t in objects_list:
        for u in t.elements:
            t.cant_ad += u.cant_fem_a + u.cant_masc_a
            t.cant_cu += u.cant_fem_c + u.cant_masc_c
            t.cant_op += u.cant_fem_o + u.cant_masc_o
            t.cant_te += u.cant_fem_t + u.cant_masc_t
            t.cant_se += u.cant_fem_s + u.cant_masc_s

    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, "edad_promedio": edad_promedio, "fecha_creacion": fecha, 'dia': dia}


def cant_trab_35(request):
    context = _request_cant_trab_35()
    context['title'] = "Total hasta 35 anos"
    template_name = 'reports/cant_trab_35.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_cant_trab_35():
    queryset = UnidadOrg.objects.all()
    objects_list = []
    menor_35 = []
    for i in queryset:
        lis_trab = Alta.objects.filter(unidad_org_id=i.id).annotate(dpto_nombre=F('departamento__nombre'))
        temp = i.nombre
        for n in lis_trab:
            var = int(n.age_by_ci[0:2])
            if var <= 35:
                menor_35.append(List_Edades(nombre= n.nombre_completo, edad=int(n.age_by_ci[0:2]), sexo=n.sexo, unidad=n.unidad_org_id,
                                        dpto=n.dpto_nombre, escolaridad=n.escolaridad,ci=n.ci, cargo=n.cargo,
                                        salario=n.salario_total_reforma, cat=n.categoria))
        elements = sorted(menor_35,key=lambda menor_35: menor_35.edad)
        objects_list.append(ListPadre(nombre=temp, elements=elements, cant_fem=0, cant_masc=0,
                                      total=elements.__len__(), iden=0))
        menor_35 = []
    objects_list = list(objects_list)
    total = 0
    for r in objects_list:
        total += r.total
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": objects_list, 'total': total, 'fecha_creacion': fecha, 'dia': dia}


def entrada_micons_empresa(request):
    context = _request_entrada_micons_empresa()
    context['title'] = "Entrada al MICONS y a VERTICE"
    template_name = 'reports/entrada_micons_empresa.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_entrada_micons_empresa():
    queryset = Alta.objects.all().values('primer_nombre', 'segundo_nombre','apellidos', 'fecha_contrato', 'fecha_alta',
                                         'fecha_ingreso').order_by('fecha_ingreso')
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)
    return {"object_list": queryset, "fecha_creacion": fecha, "dia": dia}


def preview_relacion_trabajadores(request):
    context = _request_relacion_trabajadores()
    context['title'] = "Relación de Trabajadores"
    template_name = 'reports/relacion_trabajadores_preview.html'
    context['export_pdf'] = 'relacion_trabajadores_report'
    return render(request, template_name, context)


def export_relacion_trabajadores(request):
    context = _request_relacion_trabajadores()
    context['title'] = "Relacion de Trabajadores"
    template_name = 'reports/relacion_trabajadores.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_relacion_trabajadores():
    unidades = UnidadOrg.objects.all()
    list_dpto = []
    personas = []
    objects_list = []
    for uni in unidades:
        dpto = Alta.objects.filter(unidad_org_id=uni.id).annotate(dpto_nombre=F('departamento__nombre'),
                                                                 codigo=F('departamento__codigo')).values('dpto_nombre',
                                                                                                          'codigo',
                                                                                                          'unidad_org_id',
                                                                                                          'departamento_id').order_by('departamento__codigo')
        list_ord = list(dpto.distinct('codigo'))
        for a in list_ord:
            temp = Alta.objects.filter(departamento_id=a['departamento_id'], unidad_org_id= uni.id).order_by('org_plantilla')
            for n in temp:
                personas.append(List_Edades(nombre=n.nombre_completo, edad=int(n.age_by_ci[0:2]), sexo=n.sexo, unidad=n.unidad_org_id,
                             dpto=n.departamento_id, escolaridad=n.escolaridad, ci=n.ci, cargo=n.cargo,
                             salario=n.salario_total_reforma, cat=n.categoria))
            list_dpto.append(Contrato(nombre=a['dpto_nombre'],no=personas.__len__(), personal=personas))
            personas = []
        objects_list.append(Contrato(nombre=uni.nombre,no=0, personal=list_dpto))
        list_dpto = []
    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)

    return {"object_list": objects_list, "fecha_creacion": fecha, "dia": dia }


def relacion_trab_edades(request):
    context = _request_relacion_trab_edades()
    context['title'] = "Relación de Trabajadores por Edades"
    template_name = 'reports/relacion_trab_edades.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_relacion_trab_edades():
    temporal = Alta.objects.all().annotate(dpto_nombre=F('departamento__nombre'), unidad=F('unidad_org__nombre'))
    elements = []
    for n in temporal:
        elements.append(List_Edades(nombre=n.nombre_completo, edad=int(n.age_by_ci[0:2]), sexo=n.sexo, unidad=n.unidad,
                           dpto=n.dpto_nombre, escolaridad=n.escolaridad, ci=n.ci, cargo=n.cargo,
                           salario=n.salario_total_reforma, cat=n.categoria))
    objects_list = sorted(elements, key=lambda elements: elements.edad)

    for k in objects_list:
        temp = UnidadOrg.objects.filter(nombre=k.unidad).get().siglas
        k.unidad = temp

    objects_list = list(objects_list)
    fecha_creacion = datetime.datetime.now()

    return {"object_list": objects_list, "fecha_creacion": fecha_creacion}

def relacion_trab_edades(request):
    context = _request_relacion_trab_edades()
    context['title'] = "Relacion Trabajadores por Edades"
    template_name = 'reports/relacion_trab_edades.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_relacion_trab_edades():
    temporal = Alta.objects.all().annotate(dpto_nombre=F('departamento__nombre'), unidad=F('unidad_org__nombre'))
    elements = []
    for n in temporal:
        elements.append(List_Edades(nombre=n.nombre_completo, edad=int(n.age_by_ci[0:2]), sexo=n.sexo, unidad=n.unidad,
                           dpto=n.dpto_nombre, escolaridad=n.escolaridad, ci=n.ci, cargo=n.cargo,
                           salario=n.salario_total_reforma, cat=n.categoria))
    objects_list = sorted(elements, key=lambda elements: elements.edad)

    for k in objects_list:
        temp = UnidadOrg.objects.filter(nombre=k.unidad).get().siglas
        k.unidad = temp

    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)

    return {"object_list": objects_list, "fecha_creacion": fecha, "dia": dia}


def nombre_dia_semana (fecha):
    nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    dia = nombre_dia[fecha.weekday()] + ','
    return dia

@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def empresarial_preview(request):
    context = _request_empresarial()
    context['title'] = "CANTIDAD DE TRABAJADORES POR GRUPO DE ESCALA SALARIAL Y SEXO"
    template_name = 'reports/empresarial_preview.html'
    context['export_pdf'] = 'empresarial_report'
    return render(request, template_name, context)


@permission_required('ges_trab.read_trabajador', login_url='home_principal')
def export_empresarial(request):
    context = _request_empresarial()
    context['title'] = "Empresarial"
    template_name = 'reports/empresarial.html'

    return generate_pisa_report(context, template_name, context['title'])



def _request_empresarial():
    queryset = EscalaSalarialReforma.objects.all().order_by('salario_escala')
    objects_list = []
    total_a = Alta.objects.filter(categoria='A').count()
    total_c = Alta.objects.filter(categoria='C').count()
    total_o = Alta.objects.filter(categoria='O').count()
    total_s = Alta.objects.filter(categoria='S').count()
    total_t = Alta.objects.filter(categoria='T').count()
    total_a_m = Alta.objects.filter(categoria='A', sexo='F').count()
    total_c_m = Alta.objects.filter(categoria='C', sexo='F').count()
    total_o_m = Alta.objects.filter(categoria='O', sexo='F').count()
    total_s_m = Alta.objects.filter(categoria='S', sexo='F').count()
    total_t_m = Alta.objects.filter(categoria='T', sexo='F').count()
    total = Alta.objects.all().count()
    mujeres = Alta.objects.filter(sexo='F').count()
    for item in queryset:
        operar = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='O').count()
        mujer_op = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='O', sexo='F').count()
        serv = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='S').count()
        mujer_serv = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='S', sexo='F').count()
        admin = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='A').count()
        mujer_adm = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='A', sexo='F').count()
        tecnic = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='T').count()
        mujer_tec = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='T', sexo='F').count()
        cuadro = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='C').count()
        mujer_cuad = Alta.objects.filter(escala_salarial_ref_id=item.id, categoria='C', sexo='F').count()
        total_grupo = Alta.objects.filter(escala_salarial_ref_id=item.id).count()
        mujeres_grupo = Alta.objects.filter(escala_salarial_ref_id=item.id, sexo='F').count()
        objects_list.append(Empresarial(grupo=item.grupo, salario_esc=item.salario_escala_53, operar=operar,
                                        mujer_op=mujer_op, serv=serv, mujer_serv=mujer_serv, admin=admin,
                                        mujer_adm=mujer_adm, tecnic=tecnic, mujer_tec=mujer_tec, cuadro=cuadro,
                                        mujer_cuad=mujer_cuad, total_grupo=total_grupo, mujeres=mujeres_grupo))

    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)

    maestria = Alta.objects.filter(cat_cient='2').count()
    doctorado = Alta.objects.filter(cat_cient='3').count()
    noc_I = Alta.objects.filter(escala_salarial_ref_id= 1, cargo_id = 26).count()
    noc_II = Alta.objects.filter(escala_salarial_ref_id=2, cargo_id = 26).count()
    var1 = Alta.objects.filter(escala_salarial_ref_id=1)
    con_lab_a_1 = 0
    for i in var1:
        if i.sal_cond_anor > 0.00:
            con_lab_a_1 += 1
    var2 = Alta.objects.filter(escala_salarial_ref_id=2)
    con_lab_a_2 = 0
    for i in var2:
        if i.sal_cond_anor > 0.00:
            con_lab_a_2 += 1
    var3 = Alta.objects.filter(escala_salarial_ref_id=3)
    con_lab_a_3 = 0
    for i in var3:
        if i.sal_cond_anor > 0.00:
            con_lab_a_3 += 1
    var4 = Alta.objects.filter(escala_salarial_ref_id=4)
    con_lab_a_4 = 0
    for i in var4:
        if i.sal_cond_anor > 0.00:
            con_lab_a_4 += 1
    var5 = Alta.objects.filter(escala_salarial_ref_id=5)
    con_lab_a_5 = 0
    for i in var5:
        if i.sal_cond_anor > 0.00:
            con_lab_a_5 += 1

    return {"object_list": objects_list, "total_a": total_a, "total_c": total_c, "total_o": total_o,
            "total_s": total_s, "total_t": total_t, 'fecha_creacion': fecha, 'dia': dia, "total_a_m": total_a_m,
            "total_c_m": total_c_m, "total_o_m": total_o_m, "total_s_m": total_s_m, "total_t_m": total_t_m,
            'total': total, 'mujeres': mujeres, 'maestria': maestria, 'doctorado': doctorado, 'noc_I': noc_I,
            'noc_II': noc_II, 'con_lab_a_1': con_lab_a_1, 'con_lab_a_2': con_lab_a_2, 'con_lab_a_3': con_lab_a_3,
            'con_lab_a_4': con_lab_a_4, 'con_lab_a_5': con_lab_a_5}

def chequeo_medico(request):
    unidad_org = UnidadOrg.objects.all()
    departamento = Departamento.objects.all()
    if request.method == 'GET':
        return render(
            request, 'reports/Chequeo_Medico.html',
            {'unidad_org': unidad_org, 'departamento': departamento}
        )
    unidad_org = request.POST.get('unidad', None)
    departamento = request.POST.get('departamento', None)
    if departamento == '0':
        movimientos_list = Trabajador.objects.filter(unidad_org_id=unidad_org, fecha_baja__isnull=True).annotate(
            dpto_nombre=F('departamento__nombre'), unidad=F('unidad_org__nombre'), nombre_cargo=F('cargo__nombre')
        )

    else:
        movimientos_list = Trabajador.objects.filter(unidad_org_id=unidad_org, fecha_baja__isnull=True,
                                                     departamento_id=departamento).annotate(
            dpto_nombre=F('departamento__nombre'), unidad=F('unidad_org__nombre'), nombre_cargo=F('cargo__nombre')
        )
    tipo_doc = request.POST['tipo_documento']
    if tipo_doc == '1':
        movimientos_list = movimientos_list.filter(nombre_cargo__contains='Chofer')
        template_path = 'reports/Modelo_Chequeo_Medico_Especializado.html'
        context = {'movimientos_list': movimientos_list,
                   'title': f'Chequeo Medico Especializado'}
        return generate_pisa_report(context, template_path, context['title'])
    elif tipo_doc == '2':
        template_path = 'reports/Modelo_Chequeo_Medico.html'
        context = {'movimientos_list': movimientos_list,
                   'title': f'Chequeo Medico'}
        return generate_pisa_report(context, template_path, context['title'])
    return redirect('rechum_home')

def exportar_chequeo_medico(request, pk):
    movimientos_list = Trabajador.objects.filter(id=pk).annotate(
            dpto_nombre=F('departamento__nombre'), unidad=F('unidad_org__nombre'), nombre_cargo=F('cargo__nombre'))

    template_path = 'reports/Modelo_Chequeo_Medico.html'
    context = {'movimientos_list': movimientos_list,
               'title': f'Chequeo Medico'}
    return generate_pisa_report(context, template_path, context['title'])


def exportar_chequeo_medicoesp(request, pk):
    movimientos_list = Trabajador.objects.filter(id=pk).annotate(
        dpto_nombre=F('departamento__nombre'), unidad=F('unidad_org__nombre'), nombre_cargo=F('cargo__nombre'))

    template_path = 'reports/Modelo_Chequeo_Medico_Especializado.html'
    context = {'movimientos_list': movimientos_list,
               'title': f'Chequeo Medico Especializado'}
    return generate_pisa_report(context, template_path, context['title'])


def trab_direccion(request):
    context = _request_direccion_export()
    context['title'] = "Relación de trabajadores por área y dirección particular"
    template_name = 'reports/trab_direccion_preview.html'
    context['export_pdf'] = 'trab_direccion_report'
    return render(request, template_name, context)


def trab_direccion_export(request):
    context = _request_direccion_export()
    context['title'] = "Relacion de Trabajadores por direccion"
    template_name = 'reports/trab_direccion.html'
    return generate_pisa_report(context, template_name, context['title'])


def _request_direccion_export():
    unidades = UnidadOrg.objects.all()
    list_dpto = []
    personas = []
    objects_list = []
    for uni in unidades:
        dpto = Alta.objects.filter(unidad_org_id=uni.id).annotate(
            dpto_nombre=F('departamento__nombre'), codigo=F('departamento__codigo')).values(
            'dpto_nombre', 'codigo', 'unidad_org_id', 'departamento_id').order_by('departamento__codigo')
        list_ord = list(dpto.distinct('codigo'))
        for a in list_ord:
            temp = Alta.objects.filter(departamento_id=a['departamento_id'],
                                       unidad_org_id=uni.id).order_by('org_plantilla')
            for n in temp:
                personas.append(List_Edades(nombre=n.nombre_completo, edad=int(n.age_by_ci[0:2]), sexo=n.sexo,
                                            unidad=n.unidad_org_id, dpto=n.departamento_id, escolaridad=n.escolaridad,
                                            ci=n.ci, cargo=n.cargo, salario=n.salario_total_reforma, cat=n.direccion))
            list_dpto.append(Contrato(nombre=a['dpto_nombre'], no=personas.__len__(), personal=personas))
            personas = []
        objects_list.append(Contrato(nombre=uni.nombre, no=0, personal=list_dpto))
        list_dpto = []
    objects_list = list(objects_list)
    fecha = datetime.datetime.now()
    dia = nombre_dia_semana(fecha)

    return {"object_list": objects_list, "fecha_creacion": fecha, "dia": dia}