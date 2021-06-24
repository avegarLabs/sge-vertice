from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from django.contrib.auth.decorators import login_required




urlpatterns = [
    path('', TemplateView.as_view(template_name='entrada-datos_home.html'), name='entrada-datos_home'),
    path('home_ent_dat/', login_required(views.home_ent_dat), name='home_ent_dat'),
    # path('actividad/', login_required(views.gestionar_actividad), name='gestionarActividad'),
    # path('tipo_actividad/', login_required(views.gestionar_tipo_actividad), name='gestionarTipoActividad'),
    # path('area/', login_required(views.gestionar_area), name='gestionarArea'),
    # path('servicio/', login_required(views.gestionar_servicio), name='gestionarServicio'),
    # path('orden_trabajo/', login_required(views.gestionar_ot), name='gestionarOT'),
    # path('adicionar_actividad/', login_required(views.adicionar_actividad), name='adicionarActividad'),
    # path('adicionar_area/', login_required(views.adicionar_area), name='adicionarArea'),
    # path('adicionar_servicio/', login_required(views.adicionar_servicio), name='adicionarServicio'),
    # path('adicionar_tipo_actividad/', login_required(views.adicionar_tipo_actividad), name='adicionarTipoActividad'),
    path('adicionar_suplemento/', login_required(views.adicionar_suplemento), name='adicionarSuplemento'),
    # path('editar_actividad/<int:pk>/', login_required(views.editar_actividad), name='editarActividad'),
    # path('eliminar_area/<int:pk>/', login_required(views.eliminar_area), name='eliminarArea'),
    # path('eliminar_servicio/<int:pk>/', login_required(views.eliminar_servicio), name='eliminarServicio'),
    # path('eliminar_actividad/<int:pk>/', login_required(views.eliminar_actividad), name='eliminarActividad'),
    # path('eliminar_tipo_actividad/<int:pk>/', login_required(views.eliminar_tipo_actividad),
    #      name='eliminarTipoActividad'),
    # path('inversionista/', login_required(views.gestionar_inversionista), name='gestionarInversionista'),
    # path('adicionar_inversionista/', login_required(views.adicionar_inversionista), name='adicionarInversionista'),
    # path('editar_inversionista/<int:pk>/', login_required(views.editar_inversionista), name='editarInversionista'),
    # path('eliminar_inversionista/<int:pk>/', login_required(views.eliminar_inversionista),
    #      name='eliminarInversionista'),
    # path('detalle_inversionista/<int:pk>/', login_required(views.DetalleInversionista.as_view()),
    #      name='detalleInversionista'),
    # path('orden_trabajo/', login_required(views.gestionar_ot), name='gestionarOT'),
    # path('adicionar_ot/', login_required(views.adicionar_ot), name='adicionarOT'),
    # path('editar_ot/<int:pk>/', login_required(views.editar_ot), name='editarOT'),
    # path('eliminar_ot/<int:pk>/', login_required(views.eliminar_ot),
    #      name='eliminarOT'),
    # path('detalle_ot/<int:pk>/', login_required(views.detalle_ot), name='detalleOT'),
    path('listado_suplementos/<int:pk>/', login_required(views.listado_suplementos), name='listadoSup'),

    path('inversionista/', include([
        path('', views.InvListView.as_view(), name='inversionista_list'),
        path('<str>', views.InvListView.as_view(extra_context={'errores': 'errors'}), name='inversionista_list'),
        path('agregar/', views.InvCreateView.as_view(), name='inversionista_create'),
        path('<int:pk>/actualizar/', views.InvUpdateView.as_view(), name='inversionista_update'),
        path('<int:pk>/eliminar/', views.InvDeleteView.as_view(), name='inversionista_delete'),
        path('<int:pk>/', views.InvDetailView.as_view(), name='inversionista_detail')
    ])),

    path('area/', include([
        path('', views.AreaListView.as_view(), name='area_list'),
        path('agregar/', views.AreaCreateView.as_view(), name='area_create'),
        path('<int:pk>/actualizar/', views.AreaUpdateView.as_view(), name='area_update'),
        path('<int:pk>/eliminar/', views.AreaDeleteView.as_view(), name='area_delete'),
        path('<int:pk>/', views.AreaDetailView.as_view(), name='area_detail')
    ])),
    path('servicio/', include([
        path('', views.ServListView.as_view(), name='servicio_list'),
        path('agregar/', views.ServCreateView.as_view(), name='servicio_create'),
        path('<int:pk>/actualizar/', views.ServUpdateView.as_view(), name='servicio_update'),
        path('<int:pk>/eliminar/', views.ServDeleteView.as_view(), name='servicio_delete'),
        path('<int:pk>/', views.ServDetailView.as_view(), name='servicio_detail')
    ])),
    path('orden-de-trabajo/', include([
        path('', views.OTListView.as_view(), name='ot_list'),
        path('agregar/', views.OTCreateView.as_view(), name='ot_create'),
        path('<int:pk>/actualizar/', views.OTUpdateView.as_view(), name='ot_update'),
        path('<int:pk>/eliminar/', views.OTDeleteView.as_view(), name='ot_delete'),
        path('<int:pk>/', views.OTDetailView.as_view(), name='ot_detail')
    ])),
    path('tipo-actividad/', include([
        path('', views.TipoActListView.as_view(), name='tipoactividad_list'),
        path('agregar/', views.TipoActCreateView.as_view(), name='tipoactividad_create'),
        path('<int:pk>/actualizar/', views.TipoActUpdateView.as_view(), name='tipoactividad_update'),
        path('<int:pk>/eliminar/', views.TipoActDeleteView.as_view(), name='tipoactividad_delete'),
        path('<int:pk>/', views.TipoActDetailView.as_view(), name='tipoactividad_detail')
    ])),
    path('actividad/', include([
        path('', views.ActListView.as_view(), name='actividad_list'),
        path('agregar/', views.ActCreateView.as_view(), name='actividad_create'),
        path('<int:pk>/actualizar/', views.ActUpdateView.as_view(), name='actividad_update'),
        path('<int:pk>/eliminar/', views.ActDeleteView.as_view(), name='actividad_delete'),
        path('<int:pk>/', views.ActDetailView.as_view(), name='actividad_detail')
    ])),

]
