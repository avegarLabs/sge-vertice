from distutils.command.clean import clean
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django_select2.forms import ModelSelect2Widget

from .models import Plantilla
from adm.models import UnidadOrg, Cargo
from ges_trab.models import Trabajador
from prenomina15.models import PlantillaServicio



class PlantillaForm(forms.ModelForm):
    unidad = forms.ChoiceField(choices=UnidadOrg.objects.values_list('id', 'nombre'))

    def clean(self):
        cantidad_plazas = self.cleaned_data["cant_plazas"]
        cargo = self.cleaned_data["cargo"]
        departamento = self.cleaned_data["departamento"]
        cantidad_plazas_cubiertas = Trabajador.objects.filter(
            cargo_id = cargo, departamento_id = departamento).exclude(fecha_baja__isnull=False).count()
        
        if cantidad_plazas and departamento and cargo:        
            if(cantidad_plazas < cantidad_plazas_cubiertas):
                self.add_error("cant_plazas", "La cantidad de plazas es menor a la cantidad de plazas cubiertas.")                
    class Meta:
        model = Plantilla
        fields = ('cargo', 'cant_plazas', 'escala_salarial', 'departamento')
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': 'Los campos %(field_labels)s de %(model_name)s no son únicos.'
            }
        }

   
            
        

class PlantillaServicioForm(forms.ModelForm):
    cargo = forms.ModelChoiceField(
        label=u'Cargo',
        queryset=Cargo.objects.all(),
        widget=ModelSelect2Widget(
            model=Cargo,
            search_fields=['nombre__icontains']
        )
    )

    class Meta:
        model = PlantillaServicio
        fields = ['servicio', 'cargo', 'especialidad', 'escala_salarial', 'cant_plazas']
