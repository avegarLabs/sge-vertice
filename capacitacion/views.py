from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from capacitacion.form import ActividadCapacitacionForm ,ActividadCapacitacionTrabajadoresForm
from .models import *
from principal.decorators import module_permission_required
from rechum.views import SgeListView, SgeCreateView, SgeUpdateView, SgeDetailView, SgeDeleteView


@module_permission_required('capacitacion')
def home(request):

    capacitaciones = ActividadCapacitacionTrabajadores.objects.all()
    for cap in capacitaciones:
        if ActividadCapacitacion.objects.filter(codigo=cap.actividad.codigo).count() == 0:
            print(cap.actividad.codigo)
        # capacitaciones_new = ActividadCapacitacionTrabajadores_new()
        # capacitaciones_new.actividad = ActividadCapacitacion_new.objects.filter(codigo=cap.actividad.codigo).get()
        # capacitaciones_new.trabajador = cap.trabajador
        # capacitaciones_new.save()

    print('Hola mundo')
    return render(request, 'home_cap.html')

def actualizar_datos(request):
    print('Holassss')
    # capacitaciones = ActividadCapacitacionTrabajadores.objects.all()
    # for cap in capacitaciones:
    #     actividad = ActividadCapacitacion_new.objects.filter(codigo=cap.actividad).get().pk
    #     capacitaciones_new = ActividadCapacitacionTrabajadores_new()
    #     capacitaciones_new.actividad = actividad
    #     capacitaciones_new.trabajador = cap.trabajador
    #     capacitaciones_new.save()
    #     print(cap)
    return render(request, 'home_cap.html')

# Actividad Capacitación
# Listar
class ModoFormacionListView(SgeListView):
    permission_required = 'capacitacion.read_modoformacion'
    raise_exception = True
    model = ModoFormacion
    template_name = 'mod-form/list.html'


# Crear
class ModoFormacionCreateView(SgeCreateView):
    permission_required = 'capacitacion.add_modoformacion'
    model = ModoFormacion
    fields = '__all__'
    template_name = 'mod-form/create.html'
    success_url = reverse_lazy('modoformacion_create')


# Editar
class ModoFormacionUpdateView(SgeUpdateView):
    permission_required = 'capacitacion.change_modoformacion'
    model = ModoFormacion
    fields = '__all__'
    template_name = 'mod-form/create.html'
    success_url = reverse_lazy('modoformacion_list')


# Detalle
class ModoFormacionDetailView(SgeDetailView):
    permission_required = 'capacitacion.read_modoformacion'
    model = ModoFormacion
    template_name = 'mod-form/detail.html'


# Delete
class ModoFormacionDeleteView(SgeDeleteView):
    permission_required = 'capacitacion.delete_modoformacion'
    model = ModoFormacion
    success_url = reverse_lazy('modoformacion_list')


# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////

# Tipos de Actividad de Capacitación
# Listar
class TipoActividadCapacitacionListView(SgeListView):
    permission_required = 'capacitacion.read_tipoactividadcapacitacion'
    raise_exception = True
    model = TipoActividadCapacitacion
    template_name = 'tipo-act-cap/list.html'


# Crear
class TipoActividadCapacitacionCreateView(SgeCreateView):
    permission_required = 'capacitacion.add_tipoactividadcapacitacion'
    model = TipoActividadCapacitacion
    fields = '__all__'
    template_name = 'tipo-act-cap/create.html'
    success_url = reverse_lazy('tipoactividadcapacitacion_create')


# Editar
class TipoActividadCapacitacionUpdateView(SgeUpdateView):
    permission_required = 'capacitacion.change_tipoactividadcapacitacion'
    model = TipoActividadCapacitacion
    fields = '__all__'
    template_name = 'tipo-act-cap/create.html'
    success_url = reverse_lazy('tipoactividadcapacitacion_list')


# Detalle
class TipoActividadCapacitacionDetailView(SgeDetailView):
    permission_required = 'capacitacion.read_tipoactividadcapacitacion'
    model = TipoActividadCapacitacion
    template_name = 'tipo-act-cap/detail.html'


# Delete
class TipoActividadCapacitacionDeleteView(SgeDeleteView):
    permission_required = 'capacitacion.delete_actividadcapacitacion'
    model = TipoActividadCapacitacion
    success_url = reverse_lazy('tipoactividadcapacitacion_list')


# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////

# Actividad Capacitación
# Listar
class ActividadCapacitacionListView(SgeListView):
    permission_required = 'capacitacion.read_actividadcapacitacion'
    raise_exception = True
    model = ActividadCapacitacion
    template_name = 'act-cap/list.html'


# Crear
class ActividadCapacitacionCreateView(SgeCreateView):
    permission_required = 'capacitacion.add_actividadcapacitacion'
    model = ActividadCapacitacion
    form_class = ActividadCapacitacionForm
    template_name = 'act-cap/create.html'
    success_url = reverse_lazy('actividadcapacitacion_create')




# Editar
class ActividadCapacitacionUpdateView(SgeUpdateView):
    permission_required = 'capacitacion.change_actividadcapacitacion'
    model = ActividadCapacitacion
    form_class = ActividadCapacitacionForm
    template_name = 'act-cap/create.html'
    success_url = reverse_lazy('actividadcapacitacion_list')


# Detalle
class ActividadCapacitacionDetailView(SgeDetailView):
    permission_required = 'capacitacion.read_actividadcapacitacion'
    model = ActividadCapacitacion
    template_name = 'act-cap/detail.html'


# Delete
class ActividadCapacitacionDeleteView(SgeDeleteView):
    permission_required = 'capacitacion.delete_actividadcapacitacion'
    model = ActividadCapacitacion
    success_url = reverse_lazy('actividadcapacitacion_list')


# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////

# Actividad Capacitación
# Listar
class ActividadCapacitacionTrabajadoresListView(SgeListView):
    permission_required = 'capacitacion.read_actividadcapacitaciontrabajadores'
    model = ActividadCapacitacionTrabajadores
    template_name = 'act-cap-trab/list.html'
    raise_exception = True
    queryset = ActividadCapacitacionTrabajadores.objects.all()

    def get_context_data(self, *, object_list=None, codigo_actividad=None, **kwargs):
        queryset = self.get_queryset()
        if self.kwargs['codigo_actividad']:
            codigo_actividad = self.kwargs['codigo_actividad']
        else:
            codigo_actividad = self.codigo_actividad
        object_list = queryset.filter(actividad=codigo_actividad).order_by()
        return super().get_context_data(object_list=object_list, codigo_actividad=codigo_actividad, **kwargs)

class ActividadCapacitacionTrabajadoresListView_before_deleted(SgeListView):
    permission_required = 'capacitacion.read_actividadcapacitaciontrabajadores'
    model = ActividadCapacitacionTrabajadores
    template_name = 'act-cap-trab/list.html'
    raise_exception = True
    queryset = ActividadCapacitacionTrabajadores.objects.all()

    def get_context_data(self, *, object_list=None, pk=None, **kwargs):
        queryset = self.get_queryset()
        pk = self.kwargs['pk']
        codigo_actividad = ActividadCapacitacionTrabajadores.objects.get(pk=pk).actividad.codigo
        object_list = queryset.filter(actividad=codigo_actividad).order_by()
        return super().get_context_data(object_list=object_list, **kwargs)

# Crear
class ActividadCapacitacionTrabajadoresCreateView(SgeCreateView):
    permission_required = 'capacitacion.add_actividadcapacitaciontrabajadores_new'
    model = ActividadCapacitacionTrabajadores
    # fields = '__all__'
    form_class = ActividadCapacitacionTrabajadoresForm
    template_name = 'act-cap-trab/create.html'
    success_url = reverse_lazy('actividadcapacitaciontrabajadores_create')

    # def get_success_url(self):
    #       codigo_actividad = ActividadCapacitacionTrabajadores.objects.get(pk=self.kwargs['pk']).actividad.codigo
    #       return reverse_lazy('actividadcapacitaciontrabajadores_create', kwargs={'codigo_actividad': codigo_actividad})

    def get_context_data(self, *, object_list=None, codigo_actividad=None, **kwargs):
        context = super(ActividadCapacitacionTrabajadoresCreateView, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        codigo_actividad = self.kwargs['codigo_actividad']
        form = self.form_class(self.request.GET)
        form.fields['actividad'].queryset = ActividadCapacitacion.objects.filter(pk=codigo_actividad)
        object_list = queryset.filter(actividad=codigo_actividad).order_by()
        return super().get_context_data(object_list=object_list, codigo_actividad=codigo_actividad, form=form, **kwargs)

    def get_success_url(self):
          codigo_actividad = self.kwargs['codigo_actividad']
          return reverse_lazy('actividadcapacitaciontrabajadores_create', kwargs={'codigo_actividad': codigo_actividad})

# Editar
class ActividadCapacitacionTrabajadoresUpdateView(SgeUpdateView):
    permission_required = 'capacitacion.change_actividadcapacitaciontrabajadores_new'
    model = ActividadCapacitacionTrabajadores
    form_class = ActividadCapacitacionTrabajadoresForm
    template_name = 'act-cap-trab/create.html'
    success_url = reverse_lazy('actividadcapacitaciontrabajadores_list')

    def get_context_data(self, *, object_list=None, pk=None, **kwargs):
        queryset = self.get_queryset()
        pk = self.kwargs['pk']
        codigo_actividad = ActividadCapacitacionTrabajadores.objects.get(pk=pk).actividad.codigo
        object_list = queryset.filter(actividad=codigo_actividad).order_by()
        return super().get_context_data(object_list=object_list, pk=pk, codigo_actividad=codigo_actividad, **kwargs)

    def get_success_url(self):
          codigo_actividad = ActividadCapacitacionTrabajadores.objects.get(pk=self.kwargs['pk']).actividad.codigo
          return reverse_lazy('actividadcapacitaciontrabajadores_list', kwargs={'codigo_actividad': codigo_actividad})

# Detalle
class ActividadCapacitacionTrabajadoresDetailView(SgeDetailView):
    permission_required = 'capacitacion.read_actividadcapacitaciontrabajadores_new'
    model = ActividadCapacitacionTrabajadores
    template_name = 'act-cap-trab/detail.html'


# Delete
class ActividadCapacitacionTrabajadoresDeleteView(SgeDeleteView):
    permission_required = 'capacitacion.delete_actividadcapacitaciontrabajadores_new'
    model = ActividadCapacitacionTrabajadores
    success_url = reverse_lazy('actividadcapacitaciontrabajadores_list')

    def get_success_url(self):
          codigo_actividad = ActividadCapacitacionTrabajadores.objects.get(pk=self.kwargs['pk']).actividad.codigo
          return reverse_lazy('actividadcapacitaciontrabajadores_list', kwargs={'codigo_actividad': codigo_actividad})


# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////

# Temática Capacitación
# Listar
class TematicaListView(SgeListView):
    permission_required = 'capacitacion.read_tematica'
    raise_exception = True
    model = Tematica
    template_name = 'tem-cap/list.html'


# Crear
class TematicaCreateView(SgeCreateView):
    permission_required = 'capacitacion.add_tematica'
    model = Tematica
    fields = '__all__'
    template_name = 'tem-cap/create.html'
    success_url = reverse_lazy('tematica_create')


# Editar
class TematicaUpdateView(SgeUpdateView):
    permission_required = 'capacitacion.change_tematica'
    model = Tematica
    fields = '__all__'
    template_name = 'tem-cap/create.html'
    success_url = reverse_lazy('tematica_list')


# Detalle
class TematicaDetailView(SgeDetailView):
    permission_required = 'capacitacion.read_tematica'
    model = Tematica
    template_name = 'tem-cap/detail.html'


# Delete
class TematicaDeleteView(SgeDeleteView):
    permission_required = 'capacitacion.delete_tematica'
    model = Tematica
    success_url = reverse_lazy('tematica_list')

# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////
# todo Hacer el resto, más la lógica que pueda llevar!
