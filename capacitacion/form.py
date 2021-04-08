from django import forms
from django_select2.forms import Select2Widget, ModelSelect2Widget
from capacitacion.models import *




# Capacitacion forms
class AbstractForm(forms.ModelForm):
    class Meta:
        abstract = True

    def _widget_class_modifier(self):
        for field in iter(self.fields):
            field.widget.attrs.update({'class': 'form-control'})


class TipoActividadCapacitacionForm(AbstractForm):
    class Meta:
        model = TipoActividadCapacitacion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TipoActividadCapacitacionForm, self).__init__(*args, **kwargs)
        self._widget_class_modifier()


class ActividadCapacitacionForm(AbstractForm):
    class Meta:
        model = ActividadCapacitacion
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.TextInput(attrs={'class':'datepicker'}),
            'fecha_term': forms.TextInput(attrs={'class':'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(ActividadCapacitacionForm, self).__init__(*args, **kwargs)
        # self._widget_class_modifier()



class ActividadCapacitacionTrabajadoresForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ActividadCapacitacionTrabajadoresForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ActividadCapacitacionTrabajadores
        fields = '__all__'
        widgets = {
            'actividad': Select2Widget,
            'trabajador': Select2Widget
        }

