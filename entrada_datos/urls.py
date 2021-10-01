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
    path('moneda/', include([
        path('', views.MonedaListView.as_view(), name='moneda_list'),
        path('agregar/', views.MonedaCreateView.as_view(), name='moneda_create'),
        path('<int:pk>/actualizar/', views.MonedaUpdateView.as_view(), name='moneda_update'),
        path('<int:pk>/eliminar/', views.MonedaDeleteView.as_view(), name='moneda_delete'),
        path('<int:pk>/', views.MonedaDetailView.as_view(), name='moneda_detail')
    ])),
    path('banco/', include([
        path('', views.BancoListView.as_view(), name='banco_list'),
        path('agregar/', views.BancoCreateView.as_view(), name='banco_create'),
        path('<int:pk>/actualizar/', views.BancoUpdateView.as_view(), name='banco_update'),
        path('<int:pk>/eliminar/', views.BancoDeleteView.as_view(), name='banco_delete'),
        path('<int:pk>/', views.BancoDetailView.as_view(), name='banco_detail')
    ])),
    path('cuenta-bancaria/', include([
        path('', views.CBancariaListView.as_view(), name='cuentabancaria_list'),
        path('agregar/', views.CBancariaCreateView.as_view(), name='cuentabancaria_create'),
        path('<int:pk>/actualizar/', views.CBancariaUpdateView.as_view(), name='cuentabancaria_update'),
        path('<int:pk>/eliminar/', views.CBancariaDeleteView.as_view(), name='cuentabancaria_delete'),
        path('<int:pk>/', views.CBancariaDetailView.as_view(), name='cuentabancaria_detail')
    ])),
    path('clientes/', include([
        path('', views.ClientesListView.as_view(), name='clientes_list'),
        path('agregar/', views.ClientesCreateView.as_view(), name='clientes_create'),
        path('<int:pk>/actualizar/', views.ClientesUpdateView.as_view(), name='clientes_update'),
        path('<int:pk>/eliminar/', views.ClientesDeleteView.as_view(), name='clientes_delete'),
        path('<int:pk>/', views.ClientesDetailView.as_view(), name='clientes_detail')
    ])),
    path('surtido/', include([
        path('', views.SurtidoListView.as_view(), name='surtido_list'),
        path('agregar/', views.SurtidoCreateView.as_view(), name='surtido_create'),
        path('<int:pk>/actualizar/', views.SurtidoUpdateView.as_view(), name='surtido_update'),
        path('<int:pk>/eliminar/', views.SurtidoDeleteView.as_view(), name='surtido_delete'),
        path('<int:pk>/', views.SurtidoDetailView.as_view(), name='surtido_detail')
    ])),
    path('programa/', include([
        path('', views.ProgramaListView.as_view(), name='programa_list'),
        path('agregar/', views.ProgramaCreateView.as_view(), name='programa_create'),
        path('<int:pk>/actualizar/', views.ProgramaUpdateView.as_view(), name='programa_update'),
        path('<int:pk>/eliminar/', views.ProgramaDeleteView.as_view(), name='programa_delete'),
        path('<int:pk>/', views.ProgramaDetailView.as_view(), name='programa_detail')
    ])),
    path('tipo-servicio/', include([
        path('', views.TipoServicioListView.as_view(), name='tiposervicio_list'),
        path('agregar/', views.TipoServicioCreateView.as_view(), name='tiposervicio_create'),
        path('<int:pk>/actualizar/', views.TipoServicioUpdateView.as_view(), name='tiposervicio_update'),
        path('<int:pk>/eliminar/', views.TipoServicioDeleteView.as_view(), name='tiposervicio_delete'),
        path('<int:pk>/', views.TipoServicioDetailView.as_view(), name='tiposervicio_detail')
    ])),
    path('tipo-obra/', include([
        path('', views.TipoObraListView.as_view(), name='tipoobra_list'),
        path('agregar/', views.TipoObraCreateView.as_view(), name='tipoobra_create'),
        path('<int:pk>/actualizar/', views.TipoObraUpdateView.as_view(), name='tipoobra_update'),
        path('<int:pk>/eliminar/', views.TipoObraDeleteView.as_view(), name='tipoobra_delete'),
        path('<int:pk>/', views.TipoObraDetailView.as_view(), name='tipoobra_detail')
    ])),
    path('roles/', include([
        path('', views.RolListView.as_view(), name='rol_list'),
        path('agregar/', views.RolCreateView.as_view(), name='rol_create'),
        path('<int:pk>/actualizar/', views.RolUpdateView.as_view(), name='rol_update'),
        path('<int:pk>/eliminar/', views.RolDeleteView.as_view(), name='rol_delete'),
        path('<int:pk>/', views.RolDetailView.as_view(), name='rol_detail')
    ])),
    path('solicitud-servicio/', include([
        path('', views.SolicitudServicioListView.as_view(), name='solicitudservicio_list'),
        path('agregar/', views.SolicitudServicioCreateView.as_view(), name='solicitudservicio_create'),
        path('<int:pk>/actualizar/', views.SolicitudServicioUpdateView.as_view(), name='solicitudservicio_update'),
        path('<int:pk>/eliminar/', views.SolicitudServicioDeleteView.as_view(), name='solicitudservicio_delete'),
        path('<int:pk>/', views.SolicitudServicioDetailView.as_view(), name='solicitudservicio_detail')
    ])),
    path('ofertas/', include([
        path('', views.OfertasListView.as_view(), name='ofertas_list'),
        path('agregar/', views.OfertasCreateView.as_view(), name='ofertas_create'),
        path('<int:pk>/actualizar/', views.OfertasUpdateView.as_view(), name='ofertas_update'),
        path('<int:pk>/eliminar/', views.OfertasDeleteView.as_view(), name='ofertas_delete'),
        path('<int:pk>/', views.OfertasDetailView.as_view(), name='ofertas_detail')
    ])),
    path('proyectos/', include([
        path('', views.ProyectosListView.as_view(), name='proyectos_list'),
        path('agregar/', views.ProyectosCreateView.as_view(), name='proyectos_create'),
        path('<int:pk>/actualizar/', views.ProyectosUpdateView.as_view(), name='proyectos_update'),
        path('<int:pk>/eliminar/', views.ProyectosDeleteView.as_view(), name='proyectos_delete'),
        path('<int:pk>/', views.ProyectosDetailView.as_view(), name='proyectos_detail')
    ])),
    path('contratos/', include([
        path('', views.ContratosListView.as_view(), name='contratos_list'),
        path('agregar/', views.ContratosCreateView.as_view(), name='contratos_create'),
        path('<int:pk>/actualizar/', views.ContratosUpdateView.as_view(), name='contratos_update'),
        path('<int:pk>/eliminar/', views.ContratosDeleteView.as_view(), name='contratos_delete'),
        path('<int:pk>/', views.ContratosDetailView.as_view(), name='contratos_detail')
    ])),
    path('suplementos/', include([
        path('', views.SuplementosListView.as_view(), name='suplementos_list'),
        path('agregar/', views.SuplementosCreateView.as_view(), name='suplementos_create'),
        path('<int:pk>/actualizar/', views.SuplementosUpdateView.as_view(), name='suplementos_update'),
        path('<int:pk>/eliminar/', views.SuplementosDeleteView.as_view(), name='suplementos_delete'),
        path('<int:pk>/', views.SuplementosDetailView.as_view(), name='suplementos_detail')
    ])),

]
