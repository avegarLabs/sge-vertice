from _testbuffer import ndarray
from django.contrib.auth.models import _user_has_module_perms
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import FieldError
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from rechum.views import SgeListView, SgeCreateView, SgeUpdateView, SgeDetailView, SgeDeleteView
from .form import *
from rechum.my_decorators import context_add_perm
from adm.models import UnidadOrg, Departamento



class InvListView(SgeListView):
    model = Inversionista
    template_name = 'inversionista/list.html'
    permission_required = 'entrada_datos.read_inversionista'


class InvCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_inversionista'
    model = Inversionista
    form_class = InversionistaForm
    template_name = 'inversionista/create.html'
    success_url = reverse_lazy('inversionista_create')


class InvUpdateView(SgeUpdateView):
    model = Inversionista
    form_class = InversionistaForm
    template_name = 'inversionista/create.html'
    permission_required = 'entrada_datos.change_inversionista'
    success_url = reverse_lazy('inversionista_list')


class InvDetailView(SgeDetailView):
    model = Inversionista
    template_name = 'inversionista/detail.html'
    permission_required = 'entrada_datos.read_inversionista'


class InvDeleteView(SgeDeleteView):
    model = Inversionista
    permission_required = 'entrada_datos.delete_inversionista'
    success_url = reverse_lazy('inversionista_list')


# Area
class AreaListView(SgeListView):
    model = Area
    template_name = 'area/list.html'
    permission_required = 'entrada_datos.read_area'


class AreaCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_area'
    model = Area
    form_class = AreaForm
    template_name = 'area/create.html'
    success_url = reverse_lazy('area_create')


class AreaUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_area'
    model = Area
    form_class = AreaForm
    template_name = 'area/create.html'
    success_url = reverse_lazy('area_list')


class AreaDetailView(SgeDetailView):
    model = Area
    template_name = 'area/detail.html'
    permission_required = 'entrada_datos.read_area'


class AreaDeleteView(SgeDeleteView):
    model = Area
    permission_required = 'entrada_datos.delete_area'
    success_url = reverse_lazy('area_list')

# Servicio
class ServListView(SgeListView):
    model = Servicio
    template_name = 'servicio/list.html'
    permission_required = 'entrada_datos.read_servicio'


class ServCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_servicio'
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/create.html'
    success_url = reverse_lazy('servicio_create')


class ServUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_servicio'
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/create.html'
    success_url = reverse_lazy('servicio_list')


class ServDetailView(SgeDetailView):
    model = Servicio
    template_name = 'servicio/detail.html'
    permission_required = 'entrada_datos.read_servicio'


class ServDeleteView(SgeDeleteView):
    model = Servicio
    permission_required = 'entrada_datos.delete_servicio'
    success_url = reverse_lazy('servicio_list')


# Orden de Trabajo
class OTListView(SgeListView):
    model = OT
    template_name = 'ot/list.html'
    permission_required = 'entrada_datos.read_ot'


class OTCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_ot'
    model = OT
    form_class = OTForm
    template_name = 'ot/create.html'
    success_url = reverse_lazy('ot_create')


class OTUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_ot'
    model = OT
    form_class = OTForm
    template_name = 'ot/create.html'
    success_url = reverse_lazy('ot_list')


class OTDetailView(SgeDetailView):
    model = OT
    template_name = 'ot/detail.html'
    permission_required = 'entrada_datos.read_ot'
    extra_context = {"dict": {3: 'USTI', 7: 'UGDD'}}


class OTDeleteView(SgeDeleteView):
    model = OT
    permission_required = 'entrada_datos.delete_ot'
    success_url = reverse_lazy('ot_list')


# Tipo de Actividad
class TipoActListView(SgeListView):
    model = TipoActividad
    template_name = 'tipo-actividad/list.html'
    permission_required = 'entrada_datos.read_tipoactividad'


class TipoActCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_tipoactividad'
    model = TipoActividad
    form_class = TipoActividadForm
    template_name = 'tipo-actividad/create.html'
    success_url = reverse_lazy('tipoactividad_create')


class TipoActUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_tipoactividad'
    model = TipoActividad
    form_class = TipoActividadForm
    template_name = 'tipo-actividad/create.html'
    success_url = reverse_lazy('tipoactividad_list')


class TipoActDetailView(SgeDetailView):
    model = TipoActividad
    template_name = 'tipo-actividad/detail.html'
    permission_required = 'entrada_datos.read_tipoactividad'


class TipoActDeleteView(SgeDeleteView):
    model = TipoActividad
    permission_required = 'entrada_datos.delete_tipoactividad'
    success_url = reverse_lazy('tipoactividad_list')


# Actividad
class ActListView(SgeListView):
    model = Actividad
    template_name = 'actividad/list.html'
    permission_required = 'entrada_datos.read_actividad'


class ActCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_actividad'
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad/create.html'
    success_url = reverse_lazy('actividad_create')


class ActUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_actividad'
    model = Actividad
    form_class = ActividadForm
    template_name = 'actividad/create.html'
    success_url = reverse_lazy('actividad_list')


class ActDetailView(SgeDetailView):
    model = Actividad
    template_name = 'actividad/detail.html'
    permission_required = 'entrada_datos.read_actividad'


class ActDeleteView(SgeDeleteView):  # todo no puede eliminar actividad si esta activa
    model = Actividad
    permission_required = 'entrada_datos.delete_actividad'
    success_url = reverse_lazy('actividad_list')



# Surtidos
class SurtidoListView(SgeListView):
    model = Surtidos
    template_name = 'surtidos/list.html'
    permission_required = 'entrada_datos.read_surtido'


class SurtidoCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_surtido'
    model = Surtidos
    form_class = SurtidosForm
    template_name = 'surtidos/create.html'
    success_url = reverse_lazy('surtido_create')


class SurtidoUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_surtido'
    model = Surtidos
    form_class = SurtidosForm
    template_name = 'surtidos/create.html'
    success_url = reverse_lazy('surtido_list')


class SurtidoDetailView(SgeDetailView):
    model = Surtidos
    template_name = 'surtidos/detail.html'
    permission_required = 'entrada_datos.read_surtido'


class SurtidoDeleteView(SgeDeleteView):
    model = Surtidos
    permission_required = 'entrada_datos.delete_surtido'
    success_url = reverse_lazy('surtido_list')

# Programa
class ProgramaListView(SgeListView):
    model = Programa
    template_name = 'programa/list.html'
    permission_required = 'entrada_datos.read_programa'


class ProgramaCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_programa'
    model = Programa
    form_class = ProgramaForm
    template_name = 'programa/create.html'
    success_url = reverse_lazy('programa_create')


class ProgramaUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_programa'
    model = Programa
    form_class = ProgramaForm
    template_name = 'programa/create.html'
    success_url = reverse_lazy('programa_list')


class ProgramaDetailView(SgeDetailView):
    model = Programa
    template_name = 'programa/detail.html'
    permission_required = 'entrada_datos.read_programa'


class ProgramaDeleteView(SgeDeleteView):
    model = Programa
    permission_required = 'entrada_datos.delete_programa'
    success_url = reverse_lazy('programa_list')

# Tipo Servicio
class TipoServicioListView(SgeListView):
    model = TipoServicio
    template_name = 'tipo_servicio/list.html'
    permission_required = 'entrada_datos.read_tiposervicio'


class TipoServicioCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_tiposervicio'
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'tipo_servicio/create.html'
    success_url = reverse_lazy('tiposervicio_create')


class TipoServicioUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_tiposervicio'
    model = TipoServicio
    form_class = TipoServicioForm
    template_name = 'tipo_servicio/create.html'
    success_url = reverse_lazy('tiposervicio_list')


class TipoServicioDetailView(SgeDetailView):
    model = TipoServicio
    template_name = 'tipo_servicio/detail.html'
    permission_required = 'entrada_datos.read_tiposervicio'


class TipoServicioDeleteView(SgeDeleteView):
    model = TipoServicio
    permission_required = 'entrada_datos.delete_tiposervicio'
    success_url = reverse_lazy('tiposervicio_list')

# Tipo Obra
class TipoObraListView(SgeListView):
    model = TipoObra
    template_name = 'tipo_obra/list.html'
    permission_required = 'entrada_datos.read_tipoobra'


class TipoObraCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_tipoobra'
    model = TipoObra
    form_class = TipoObraForm
    template_name = 'tipo_obra/create.html'
    success_url = reverse_lazy('tipoobra_create')


class TipoObraUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_tipoobra'
    model = TipoObra
    form_class = TipoObraForm
    template_name = 'tipo_obra/create.html'
    success_url = reverse_lazy('tipoobra_list')


class TipoObraDetailView(SgeDetailView):
    model = TipoObra
    template_name = 'tipo_obra/detail.html'
    permission_required = 'entrada_datos.read_tipoobra'


class TipoObraDeleteView(SgeDeleteView):
    model = TipoObra
    permission_required = 'entrada_datos.delete_tipoobra'
    success_url = reverse_lazy('tipoobra_list')


# Roles
class RolListView(SgeListView):
    model = Roles
    template_name = 'roles/list.html'
    permission_required = 'entrada_datos.read_rol'


class RolCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_rol'
    model = Roles
    form_class = RolesForm
    template_name = 'roles/create.html'
    success_url = reverse_lazy('rol_create')


class RolUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_rol'
    model = Roles
    form_class = RolesForm
    template_name = 'roles/create.html'
    success_url = reverse_lazy('rol_list')


class RolDetailView(SgeDetailView):
    model = Roles
    template_name = 'roles/detail.html'
    permission_required = 'entrada_datos.read_rol'


class RolDeleteView(SgeDeleteView):
    model = Roles
    permission_required = 'entrada_datos.delete_rol'
    success_url = reverse_lazy('rol_list')


# Moneda
class MonedaListView(SgeListView):
    model = Moneda
    template_name = 'moneda/list.html'
    permission_required = 'entrada_datos.read_moneda'


class MonedaCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_moneda'
    model = Moneda
    form_class = MonedaForm
    template_name = 'moneda/create.html'
    success_url = reverse_lazy('moneda_create')


class MonedaUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_moneda'
    model = Moneda
    form_class = MonedaForm
    template_name = 'moneda/create.html'
    success_url = reverse_lazy('moneda_list')


class MonedaDetailView(SgeDetailView):
    model = Moneda
    template_name = 'moneda/detail.html'
    permission_required = 'entrada_datos.read_moneda'


class MonedaDeleteView(SgeDeleteView):
    model = Moneda
    permission_required = 'entrada_datos.delete_moneda'
    success_url = reverse_lazy('moneda_list')

# Banco
class BancoListView(SgeListView):
    model = Banco
    template_name = 'banco/list.html'
    permission_required = 'entrada_datos.read_banco'


class BancoCreateView(SgeCreateView):
    permission_required = 'entrada_datos.add_banco'
    model = Banco
    form_class = BancoForm
    template_name = 'banco/create.html'
    success_url = reverse_lazy('banco_create')


class BancoUpdateView(SgeUpdateView):
    permission_required = 'entrada_datos.change_banco'
    model = Banco
    form_class = BancoForm
    template_name = 'banco/create.html'
    success_url = reverse_lazy('banco_list')


class BancoDetailView(SgeDetailView):
    model = Banco
    template_name = 'banco/detail.html'
    permission_required = 'entrada_datos.read_banco'


class BancoDeleteView(SgeDeleteView):
    model = Banco
    permission_required = 'entrada_datos.delete_banco'
    success_url = reverse_lazy('banco_list')














#@permission_required('entrada_datos','home_principal')
def home_ent_dat(request):
    # Verificando si tiene permiso para el modulo de Entrada de Datos
    permiso_app_adm = _user_has_module_perms(request.user, 'entrada_datos')
    if permiso_app_adm:
        context = {'request': request}
        return render(request, 'entrada-datos_home.html', context)
    else:
        return redirect('home_principal')



@permission_required('entrada_datos.read_inversionista','home_principal')
def gestionar_inversionista(request):
    list_inv = Inversionista.objects.all()
    form = InversionistaForm(request.POST or None)
    context = dict(request=request,
                   list_inv=list_inv,
                   form=form)
    context = context_add_perm(request, context, 'entrada_datos', 'inversionista')
    return render(request, 'Gestionar_Inversionista.html', context)


@permission_required('entrada_datos.read_area','home_principal')
def gestionar_area(request):
    areas = Area.objects.all()
    unidades = UnidadOrg.objects.all()
    form = AreaForm(request.POST or None)
    if request.POST:
        form.fields['area'].queryset = Departamento.objects.filter(dirige_id__isnull=True)
    context = {'request': request,
               'list_area': areas,
               'list_unidades': unidades,
               'form': form}
    context = context_add_perm(request, context, 'entrada_datos', 'area')
    return render(request, 'Gestionar_Area.html', context)


@permission_required('entrada_datos.read_servicio','home_principal')
def gestionar_servicio(request):
    servicio = Servicio.objects.all()
    form = ServicioForm(request.POST or None)
    context = {'list_serv': servicio, 'form': form}
    context = context_add_perm(request, context, 'entrada_datos', 'servicio')
    return render(request, 'Gestionar_Servicio.html', context)


@permission_required('entrada_datos.read_ot','home_principal')
def gestionar_ot(request):
    servicios = Servicio.objects.all()
    areas = Area.objects.all()
    list_ot = OT.objects.all()
    form = OTForm(request.POST or None)
    formsup = SuplementoForm(request.POST or None)
    context = {'list_ot': list_ot, 'form': form, 'servicios': servicios, 'areas': areas, 'formsup': formsup}
    return render(request, 'Gestionar_OT.html', context)


@permission_required('entrada_datos.read_actividad','home_principal')
def gestionar_actividad(request):
    actividades = TipoActividad.objects.all()
    list_act = Actividad.objects.all()
    form = ActividadForm(request.POST or None)
    context = {'list_act': list_act, 'form': form, 'tipo_actividades_list': actividades}
    return render(request, 'Gestionar_Actividad.html', context)


@permission_required('entrada_datos.read_actividad','home_principal')
def gestionar_tipo_actividad(request):
    tipo_act = TipoActividad.objects.all()
    form = TipoActividadForm(request.POST or None)
    context = {'tipo_act': tipo_act, 'form': form}
    return render(request, 'Gestionar_Tipo_Actividad.html', context)


@permission_required('entrada_datos.add_inversionista','home_principal')
def adicionar_inversionista(request):
    form = InversionistaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('gestionarInversionista')
    cal = Inversionista.objects.all()
    context = {'list_inv': cal, 'form': form}
    return render(request, 'Gestionar_Inversionista.html', context)


@permission_required('entrada_datos.add_area','home_principal')
def adicionar_area(request):
    form = AreaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/area/')
    list_area = Area.objects.all()
    context = {'list_area': list_area, 'form': form}
    return render(request, 'Gestionar_Area.html', context)


@permission_required('entrada_datos.add_servicio','home_principal')
def adicionar_servicio(request):
    form = ServicioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/servicio/')
    list_serv = Servicio.objects.all()
    context = {'list_serv': list_serv, 'form': form}
    return render(request, 'Gestionar_Servicio.html', context)


@permission_required('entrada_datos.add_ot','home_principal')
def adicionar_ot(request):
    servicios = Servicio.objects.all()
    areas = Area.objects.all()
    form = OTForm(request.POST or None)
    if form.is_valid():
        ot = OT(
            unidad=form.cleaned_data['unidad'],
            area=Area.objects.filter(id=request.POST['area']).get(),
            tipo_servicio=Servicio.objects.filter(id=request.POST['servicio']).get(),
            inversionista=form.cleaned_data['inversionista'],
            no_contrato=form.cleaned_data['no_contrato'],
            descripcion_ot=form.cleaned_data['descripcion_ot'],
            codigo_ot=form.cleaned_data['codigo_ot']
        )
        ot.save()
        return redirect('/orden_trabajo/')
    cal = OT.objects.all()
    context = {'list_ot': cal, 'form': form, 'servicios': servicios, 'areas': areas}
    return render(request, 'Gestionar_OT.html', context)


@permission_required('entrada_datos.add_suplemento','home_principal')
def adicionar_suplemento(request):
    form = SuplementoForm(request.POST or None)
    formot = OTForm(None)
    if form.is_valid():
        suplemento = Suplemento(
            orden_trab_id=request.POST['orden_trab'],
            monto=form.cleaned_data['monto'],
            fecha=form.cleaned_data['fecha'],
            solicitud=form.cleaned_data['solicitud'],
            usuario=request.user.first_name + ' ' + request.user.last_name,
        )
        ot = OT.objects.get(id=suplemento.orden_trab_id)
        ot.valor_contrato += suplemento.monto
        try:
            suplemento.save()
        except FieldError:
            servicios = Servicio.objects.all()
            areas = Area.objects.all()
            cal = OT.objects.all()
            context = {'list_ot': cal, 'formsup': form, 'form': formot, 'servicios': servicios, 'areas': areas,
                       'errores': 'Intentelo de nuevo. Ha ocurrido un error de Base de Datos'}
            return render(request, 'Gestionar_OT.html', context)
        except DatabaseError:
            servicios = Servicio.objects.all()
            areas = Area.objects.all()
            cal = OT.objects.all()
            context = {'list_ot': cal, 'formsup': form, 'form': formot, 'servicios': servicios, 'areas': areas,
                       'errores': 'Intentelo de nuevo. Ha ocurrido un error de Base de Datos'}
            return render(request, 'Gestionar_OT.html', context)
        ot.save()
        servicios = Servicio.objects.all()
        areas = Area.objects.all()
        cal = OT.objects.all()
        context = {'list_ot': cal, 'formsup': form, 'form': formot, 'servicios': servicios, 'areas': areas}
        return render(request, 'Gestionar_OT.html', context)
    servicios = Servicio.objects.all()
    areas = Area.objects.all()
    cal = OT.objects.all()
    context = {'list_ot': cal, 'formsup': form, 'form': formot, 'servicios': servicios, 'areas': areas}
    return render(request, 'Gestionar_OT.html', context)


@permission_required('entrada_datos.add_actividad','home_principal')
def adicionar_actividad(request):
    actividades = TipoActividad.objects.all()
    form = ActividadForm(request.POST or None)
    if form.is_valid():
        actividad = Actividad(
            orden_trab=form.cleaned_data['orden_trab'],
            tipo_act=TipoActividad.objects.filter(id=request.POST['tipo_act']).get(),
            numero=form.cleaned_data['numero'],
            descripcion_act=form.cleaned_data['descripcion_act'],
            codigo_act=form.cleaned_data['codigo_act'],
            valor_act=form.cleaned_data['valor_act']
        )
        ot = OT.objects.get(id=actividad.orden_trab.id)
        ot.valor_contrato += actividad.valor_act
        if Actividad.objects.filter(orden_trab=actividad.orden_trab, codigo_act=actividad.codigo_act).count():
            cal = Actividad.objects.all()
            context = {'list_act': cal, 'form': form, 'object': actividad, 'tipo_actividades_list': actividades,
                       'errores': 'La OT seleccionada ya tiene asignado una actividad con el mismo código.'}
            return render(request, 'Gestionar_Actividad.html', context)
        else:
            try:
                actividad.save()
            except FieldError:
                cal = Actividad.objects.all()
                context = {'list_act': cal, 'form': form, 'object': actividad, 'tipo_actividades_list': actividades,
                           'errores': 'Inténtelo de nuevo. Ha ocurrido un error de Base de Datos'}
                return render(request, 'Gestionar_Actividad.html', context)
            except DatabaseError:
                cal = Actividad.objects.all()
                context = {'list_act': cal, 'form': form, 'object': actividad, 'tipo_actividades_list': actividades,
                           'errores': 'Inténtelo de nuevo. Ha ocurrido un error de Base de Datos'}
                return render(request, 'Gestionar_Actividad.html', context)
            ot.save()
            return redirect('gestionarActividad')
    if request.method == 'POST':
        actividades = TipoActividad.objects.all()
        list_act = Actividad.objects.all()
        context = {'list_act': list_act, 'form': form, 'tipo_actividades_list': actividades}
        return render(request, 'Gestionar_Actividad.html', context)


@permission_required('entrada_datos.add_tipo_actividad','home_principal')
def adicionar_tipo_actividad(request):
    form = TipoActividadForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/tipo_actividad/')
    tipo_act = TipoActividad.objects.all()
    context = {'tipo_act': tipo_act, 'form': form}
    return render(request, 'Gestionar_Tipo_Actividad.html', context)


@permission_required('entrada_datos.change_inversionista','home_principal')
def editar_inversionista(request, pk):
    inversionista = Inversionista.objects.get(id=pk)
    form = InversionistaForm(request.POST or None, instance=inversionista)
    if form.is_valid():
        form.save()
        return redirect('/inversionista/')
    cal = Inversionista.objects.all()
    context = {'request': request,
               'list_inv': cal,
               'form': form,
               'edit': pk}
    context = context_add_perm(request, context, 'inversionista')
    return render(request, 'Gestionar_Inversionista.html', context)


@permission_required('entrada_datos.change_ot','home_principal')
def editar_ot(request, pk):
    ot = OT.objects.get(id=pk)
    form = OTForm(request.POST or None, instance=ot)
    if form.is_valid():
        form.save()
        return redirect('/orden_trabajo/')
    cal = OT.objects.all()
    context = {'list_ot': cal, 'form': form, 'edit': pk}
    return render(request, 'Gestionar_OT.html', context)


@permission_required('entrada_datos.cange_actividad','home_principal')
def editar_actividad(request, pk):
    actividades = TipoActividad.objects.all()
    actividad = Actividad.objects.get(id=pk)
    form = ActividadForm(request.POST or None, instance=actividad)
    if form.is_valid():
        form.save()
        return redirect('/actividad/')
    cal = Actividad.objects.all()
    context = {'list_act': cal, 'form': form, 'edit': pk, 'tipo_actividades_list': actividades}
    return render(request, 'Gestionar_Actividad.html', context)


@permission_required('entrada_datos.delete_inversionista','home_principal')
def eliminar_inversionista(request, pk):
    inversionista = Inversionista.objects.get(id=pk)
    if request.method == 'GET':
        context = {'object': inversionista}
        return render(request, 'Eliminar_Inversionista.html', context)
    else:
        from django.db import IntegrityError
        try:
            inversionista.delete()
            return redirect('gestionarInversionista')
        except IntegrityError:
            cal = Inversionista.objects.all()
            form = InversionistaForm(None)
            errores = 'Imposible eliminar Inversionista porque está asociado a una OT'
            context = {'request': request,
                       'list_inv': cal,
                       'form': form,
                       'errores': errores}
            context = context_add_perm(request, context, 'inversionista')

            return render(request, 'Gestionar_Inversionista.html', context)


@permission_required('entrada_datos.delete_area','home_principal')
def eliminar_area(request, pk):
    area = Area.objects.get(id=pk)
    if request.method == 'GET':
        context = {'object': area}
        return render(request, 'Eliminar_Area.html', context)
    else:
        from django.db import IntegrityError
        try:
            area.delete()
            return redirect('/area/')
        except IntegrityError:
            cal = Area.objects.all()
            form = AreaForm(None)
            context = {'list_area': cal, 'form': form,
                       'errores': 'Imposible eliminar Área porque tiene asociada al menos una OT'}
            context = context_add_perm(request, context, 'area')
            return render(request, 'Gestionar_Area.html', context)


@permission_required('entrada_datos.delete_servicio','home_principal')
def eliminar_servicio(request, pk):
    serv = Servicio.objects.get(id=pk)
    if request.method == 'GET':
        context = {'object': serv}
        return render(request, 'Eliminar_Servicio.html', context)
    else:
        from django.db import IntegrityError
        try:
            serv.delete()
            return redirect('/servicio/')
        except IntegrityError:
            cal = Servicio.objects.all()
            form = ServicioForm(None)
            context = {'list_serv': cal, 'form': form,
                       'errores': 'Imposible eliminar Servicio porque tiene asociada al menos una OT'}
            context = context_add_perm(request, context, 'servicio')
            return render(request, 'Gestionar_Servicio.html', context)


@permission_required('entrada_datos.delete_ot','home_principal')
def eliminar_ot(request, pk):
    servicios = Servicio.objects.all()
    areas = Area.objects.all()
    ot = OT.objects.get(id=pk)
    formsup = SuplementoForm(None)
    if request.method == 'GET':
        context = {'object': ot}
        return render(request, 'Eliminar_OT.html', context)
    else:
        from django.db import IntegrityError
        try:
            ot.delete()
            return redirect('/orden_trabajo/')
        except IntegrityError:
            cal = OT.objects.all()
            form = OTForm(None)
            context = {'list_ot': cal, 'form': form,
                       'errores': 'Imposible eliminar Orden de trabajo porque tiene asociado actividades',
                       'servicios': servicios, 'areas': areas, 'formsup': formsup}
            return render(request, 'Gestionar_OT.html', context)


@permission_required('entrada_datos.delete_actividad','home_principal')
def eliminar_actividad(request, pk):
    actividades = TipoActividad.objects.all()
    actividad = Actividad.objects.get(id=pk)
    if request.method == 'GET':
        context = {'object': actividad}
        return render(request, 'Eliminar_Actividad.html', context)
    else:
        from django.db import IntegrityError
        try:
            if actividad.activa:
                list_act = Actividad.objects.all()
                form = ActividadForm(None)
                context = {'list_act': list_act, 'form': form,
                           'errores': 'Imposible eliminar actividad con producción en proceso para próximo mes.',
                           'tipo_actividades_list': actividades}
                return render(request, 'Gestionar_Actividad.html', context)
            else:
                actividad.delete()
                return redirect('/actividad/')
        except IntegrityError:
            cal = Actividad.objects.all()
            form = ActividadForm(None)
            context = {'list_act': cal, 'form': form, 'errores': 'Imposible eliminar Actividad'}
            return render(request, 'Gestionar_Actividad.html', context)


@permission_required('entrada_datos.delete_tipo_actividad','home_principal')
def eliminar_tipo_actividad(request, pk):
    tipo_acti = TipoActividad.objects.get(id=pk)
    if request.method == 'GET':
        context = {'object': tipo_acti}
        return render(request, 'Eliminar_Tipo_Actividad.html', context)
    else:
        from django.db import IntegrityError
        try:
            tipo_acti.delete()
            return redirect('/tipo_actividad/')
        except IntegrityError:
            tipo_act = TipoActividad.objects.all()
            form = TipoActividadForm(None)
            context = {'tipo_act': tipo_act, 'form': form,
                       'errores': 'Imposible eliminar tipo de actividad porque tiene asociada al menos una actividad'}
            return render(request, 'Gestionar_Tipo_Actividad.html', context)


class DetalleInversionista(generic.DetailView):
    model = Inversionista
    template_name = 'Detalle_Inversionista.html'


@permission_required('entrada_datos.read_ot','home_principal')
def detalle_ot(request, pk):
    ot = OT.objects.get(id=pk)
    context = {'ot': ot}
    return render(request, 'Detalle_OT.html', context)


@permission_required('entrada_datos_read_suplemento','home_principal')
def listado_suplementos(request, pk):
    list_sup = Suplemento.objects.filter(orden_trab_id=pk)
    ot = OT.objects.get(id=pk)
    context = {'list_sup': list_sup, 'ot': ot}
    return render(request, 'Listado_Suplemento.html', context)


# //////////////////////////////////////////////////////////////////////////////////////////////





















