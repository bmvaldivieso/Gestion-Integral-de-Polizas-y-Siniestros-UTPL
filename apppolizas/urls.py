from django.urls import path

from .views import (
    AdminUsuariosView,
    BienDetailApiView,
    BienesPorCustodioView,
    CrearSiniestroDesdeReporteView,
    CustodioDetailApiView,
    CustodioListView,
    DashboardAdminView,
    DashboardAnalistaView,
    DetalleReporteExternoView,
    EnviarAseguradoraView,
    FiniquitoCreateView,
    ListaReportesExternosView,
    LoginView,
    PolizaDeleteView,
    PolizaDetailView,
    PolizaListView,
    PolizaUpdateView,
    RepararSiniestroView,
    ReporteExternoConfirmacionView,
    ReporteExternoView,
    ReporteGeneralPDFView,
    SiniestroDeleteEvidenciaView,
    SiniestroDeleteView,
    SiniestroDetailView,
    SiniestroEditView,
    SiniestroListView,
    SubirEvidenciaView,
    UsuarioCRUDView,
    buscar_bienes_ajax,
    buscar_custodios_ajax,
    crear_factura,
    generar_pdf_factura,
    lista_facturas,
    lista_notificaciones,
    logout_view,
    marcar_notificacion_leida,
)

urlpatterns = [
    # Reportes Externos (públicos)
    path("reportar-siniestro/", ReporteExternoView.as_view(), name="reporte_externo"),
    path(
        "reporte-enviado/",
        ReporteExternoConfirmacionView.as_view(),
        name="reporte_externo_confirmacion",
    ),
    # Login
    path("", LoginView.as_view(), name="login"),
    # Dashboards
    path(
        "administrador/dashboard/", DashboardAdminView.as_view(), name="dashboard_admin"
    ),
    path(
        "dashboard-analista/",
        DashboardAnalistaView.as_view(),
        name="dashboard_analista",
    ),
    # Admin
    path("administrador/usuarios/", AdminUsuariosView.as_view(), name="admin_usuarios"),
    # --- 2. NUEVA RUTA REPORTE PDF ---
    path(
        "administrador/reporte-general/",
        ReporteGeneralPDFView.as_view(),
        name="reporte_general_pdf",
    ),
    # ---------------------------------
    # API Usuarios
    path("api/usuarios/", UsuarioCRUDView.as_view(), name="usuarios_list_create"),
    path(
        "api/usuarios/<int:usuario_id>/",
        UsuarioCRUDView.as_view(),
        name="usuarios_detail",
    ),
    # Pólizas
    path("polizas/", PolizaListView.as_view(), name="polizas_list"),
    path("polizas/<int:pk>/", PolizaDetailView.as_view(), name="poliza_detail"),
    path("polizas/editar/<int:pk>/", PolizaUpdateView.as_view(), name="poliza_update"),
    path(
        "polizas/eliminar/<int:pk>/", PolizaDeleteView.as_view(), name="poliza_delete"
    ),
    # Siniestros
    path("siniestros/", SiniestroListView.as_view(), name="siniestros"),
    path(
        "siniestros/<int:pk>/", SiniestroDetailView.as_view(), name="siniestro_detail"
    ),
    path(
        "siniestros/<int:pk>/editar/",
        SiniestroEditView.as_view(),
        name="siniestro_edit",
    ),
    path(
        "siniestros/<int:pk>/eliminar/",
        SiniestroDeleteView.as_view(),
        name="siniestro_delete",
    ),
    path(
        "siniestros/<int:pk>/reparar/",
        RepararSiniestroView.as_view(),
        name="siniestro_reparar",
    ),
    path(
        "siniestros/<int:pk>/enviar_aseguradora/",
        EnviarAseguradoraView.as_view(),
        name="enviar_aseguradora",
    ),
    # Crear siniestro desde reporte externo
    path(
        "siniestros/crear-desde-reporte/<int:reporte_id>/",
        CrearSiniestroDesdeReporteView.as_view(),
        name="crear_siniestro_desde_reporte",
    ),
    # Documentos de Siniestro
    path(
        "siniestros/<int:siniestro_id>/subir_evidencia/",
        SubirEvidenciaView.as_view(),
        name="subir_evidencia",
    ),
    path(
        "documentos/<int:pk>/eliminar/",
        SiniestroDeleteEvidenciaView.as_view(),
        name="eliminar_evidencia",
    ),
    # GESTIÓN DE CUSTODIOS
    path("custodios/", CustodioListView.as_view(), name="custodios_list"),
    # API JSON para el modal de detalle custodio
    path(
        "api/custodios/<int:pk>/",
        CustodioDetailApiView.as_view(),
        name="api_custodio_detail",
    ),
    # GESTIÓN DE BIENES
    path(
        "custodios/<int:custodio_id>/bienes/",
        BienesPorCustodioView.as_view(),
        name="bienes_custodio_list",
    ),
    # API JSON para el modal de detalle bien
    path("api/bienes/<int:pk>/", BienDetailApiView.as_view(), name="api_bien_detail"),
    # GESTIÓN DE FINIQUITOS
    path(
        "siniestros/<int:siniestro_id>/finiquitar/",
        FiniquitoCreateView.as_view(),
        name="crear_finiquito",
    ),
    # GESTIÓN DE NOTIFICACIONES
    path("notificaciones/", lista_notificaciones, name="lista_notificaciones"),
    path(
        "notificaciones/leer/<int:notificacion_id>/",
        marcar_notificacion_leida,
        name="marcar_notificacion_leida",
    ),
    # Administración de Reportes Externos (privado)
    path(
        "gestion/reportes-externos/",
        ListaReportesExternosView.as_view(),
        name="reportes_externos_list",
    ),
    path(
        "gestion/reportes-externos/<int:pk>/",
        DetalleReporteExternoView.as_view(),
        name="reporte_externo_detail",
    ),
    # Buscador custodio y bienes
    path("ajax/buscar-custodios/", buscar_custodios_ajax, name="buscar_custodios_ajax"),
    path("ajax/buscar-bienes/", buscar_bienes_ajax, name="buscar_bienes_ajax"),
    # Facturas
    path("facturas/", lista_facturas, name="lista_facturas"),
    path("facturas/crear/", crear_factura, name="crear_factura"),
    path(
        "facturas/<int:factura_id>/pdf/",
        generar_pdf_factura,
        name="generar_pdf_factura",
    ),
]
