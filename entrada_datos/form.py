from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget

from .models import *
from adm.models import UnidadOrg


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['descripcion_act', 'orden_trab', 'codigo_act', 'numero', 'valor_act', 'prod_tecleada']
        widgets = {
            'orden_trab': Select2Widget,
            'tipo_act': Select2Widget
        }

    def __init__(self, *args, **kwargs):
        super(ActividadForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class InversionistaForm(forms.ModelForm):
    class Meta:
        model = Inversionista
        fields = ['codigo_inv', 'nombre_inv', 'direccion_inv', 'municipio_sucursal_inv', 'sucursal_mn_inv',
                  'sucursal_usd_inv', 'cuenta_mn_inv', 'cuenta_usd_inv', 'nit']


    def __init__(self, *args, **kwargs):
        super(InversionistaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class OTForm(forms.ModelForm):
    class Meta:
        model = OT
        fields = '__all__'
        widgets = {
            'inversionista': Select2Widget,
            'tipo_servicio': Select2Widget,
            'area': Select2Widget,
            'unidad': Select2Widget
        }

    def __init__(self, *args, **kwargs):
        super(OTForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class TipoActividadForm(forms.ModelForm):
    class Meta:
        model = TipoActividad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoActividadForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class AreaForm(forms.ModelForm):
    # unidad = forms.ModelChoiceField(UnidadOrg.objects.all(), label=u'Unidad Organizacional:', widget=Select2Widget)

    unidad = forms.ModelChoiceField(
       queryset=UnidadOrg.objects.all(),
       label=u'Unidad Organizacional:',
       widget=ModelSelect2Widget(
           model=UnidadOrg,
           search_fields=['nombre__icontains']
       )
    )

    area = forms.ModelChoiceField(
       queryset=Departamento.objects.all(),
       label=u'Área:',
       widget=ModelSelect2Widget(
           model=Departamento,
           search_fields=['nombre__icontains'],
           dependent_fields={'unidad': 'unidad'}
       )
    )



    class Meta:
        model = Area
        fields = '__all__'
        # widgets = {'area': Select2Widget}

    def __init__(self, *args, **kwargs):
        super(AreaForm, self).__init__(*args, **kwargs)
        self.fields['area'].queryset = Departamento.objects.filter(dirige_id__isnull=True)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['codigo', 'nombre']

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class SuplementoForm(forms.ModelForm):
    class Meta:
        model = Suplemento
        fields = ['monto', 'fecha', 'solicitud']

    def __init__(self, *args, **kwargs):
        super(SuplementoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class MonedaForm(forms.ModelForm):
    class Meta:
        model = Moneda
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MonedaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BancoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CuentaBancariaForm(forms.ModelForm):
    class Meta:
        model = CuentaBancaria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CuentaBancariaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class SurtidoForm(forms.ModelForm):
    class Meta:
        model = Surtido
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(SurtidoForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProgramaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TipoServicioForm(forms.ModelForm):
    class Meta:
        model = TipoServicio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoServicioForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class TipoObraForm(forms.ModelForm):
    class Meta:
        model = TipoObra
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoObraForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RolForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientesForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})