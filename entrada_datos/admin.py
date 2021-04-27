from django.contrib import admin
from .models import TipoActividad, Actividad,  OT, Inversionista, Suplemento

# Register your models here.
admin.site.register(TipoActividad)
admin.site.register(Actividad)
admin.site.register(OT)
admin.site.register(Inversionista)
admin.site.register(Suplemento)