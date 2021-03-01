from rechum.urls import *
from . import views

urlpatterns = [
    path('capacitacion/', include([
        path('', views.home, name='capacitacion_home'),
        # path('', views.actualizar_datos, name='actualizar_datos'),
        path('actividad/', include([
            path('', views.ActividadCapacitacionListView.as_view(), name="actividadcapacitacion_list"),
            path('agregar/', views.ActividadCapacitacionCreateView.as_view(), name="actividadcapacitacion_create"),
            path('<str:pk>/actualizar/', views.ActividadCapacitacionUpdateView.as_view(),
                 name="actividadcapacitacion_update"),
            path('<str:pk>/', views.ActividadCapacitacionDetailView.as_view(), name="actividadcapacitacion_detail"),
            path('<str:pk>/eliminar/', views.ActividadCapacitacionDeleteView.as_view(),
                 name="actividadcapacitacion_delete")

        ])),
        path('modo_formacion/', include([
            path('', views.ModoFormacionListView.as_view(), name='modoformacion_list'),
            path('agregar/', views.ModoFormacionCreateView.as_view(), name='modoformacion_create'),
            path('<str:pk>/', views.ModoFormacionDetailView.as_view(), name='modoformacion_detail'),
            path('<str:pk>/actualizar/', views.ModoFormacionUpdateView.as_view(), name='modoformacion_update'),
            path('<str:pk>/eliminar/', views.ModoFormacionDeleteView.as_view(), name='modoformacion_delete')
        ])),
        path('tipo_actividad/', include([
            path('', views.TipoActividadCapacitacionListView.as_view(), name='tipoactividadcapacitacion_list'),
            path('agregar/', views.TipoActividadCapacitacionCreateView.as_view(),
                 name='tipoactividadcapacitacion_create'),
            path('<str:pk>/', views.TipoActividadCapacitacionDetailView.as_view(),
                 name='tipoactividadcapacitacion_detail'),
            path('<str:pk>/actualizar/', views.TipoActividadCapacitacionUpdateView.as_view(),
                 name='tipoactividadcapacitacion_update'),
            path('<str:pk>/eliminar/', views.TipoActividadCapacitacionDeleteView.as_view(),
                 name='tipoactividadcapacitacion_delete')
        ])),
        path('tematica/', include([
            path('', views.TematicaListView.as_view(), name='tematica_list'),
            path('agregar/', views.TematicaCreateView.as_view(),
                 name='tematica_create'),
            path('<str:pk>/', views.TematicaDetailView.as_view(),
                 name='tematica_detail'),
            path('<str:pk>/actualizar/', views.TematicaUpdateView.as_view(),
                 name='tematica_update'),
            path('<str:pk>/eliminar/', views.TematicaDeleteView.as_view(),
                 name='tematica_delete')
        ])),
        path('list_trab/', include([
            path('<str:codigo_actividad>/list_trab/', views.ActividadCapacitacionTrabajadoresListView.as_view(),
                 name="actividadcapacitaciontrabajadores_list"),
            path('<str:codigo_actividad>/agregar/', views.ActividadCapacitacionTrabajadoresCreateView.as_view(),
                 name='actividadcapacitaciontrabajadores_create'),
            path('<str:pk>/', views.ActividadCapacitacionTrabajadoresDetailView.as_view(),
                 name='actividadcapacitaciontrabajadores_detail'),
            path('<str:pk>/actualizar/', views.ActividadCapacitacionTrabajadoresUpdateView.as_view(),
                 name='actividadcapacitaciontrabajadores_update'),
            path('<str:pk>/eliminar/', views.ActividadCapacitacionTrabajadoresDeleteView.as_view(),
                 name='actividadcapacitaciontrabajadores_delete')
        ]))

    ]))
]
