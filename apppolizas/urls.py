from django.urls import path
from .views import (
    LoginView,
    DashboardAdminView,
    DashboardAnalistaView,
    AdminUsuariosView,
    PolizaListView,
    PolizaUpdateView,
    PolizaDeleteView,
    PolizaDetailView,
    UsuarioCRUDView,
    logout_view,
    SiniestroListView,
    SiniestroDetailView,
    SiniestroEditView,
    SiniestroDeleteView,
<<<<<<< HEAD
    lista_facturas,
    crear_factura,
    generar_pdf_factura,
<<<<<<< Updated upstream
=======
    SubirEvidenciaView,
    SiniestroDeleteEvidenciaView, 
    CustodioListView, 
    CustodioUpdateView, 
    CustodioDeleteView,
    FiniquitoCreateView,
    lista_notificaciones,
    marcar_notificacion_leida,
>>>>>>> Stashed changes
)

=======
)


>>>>>>> 023cea205f0f0fa6e2fc75d4401f28287856a05b
urlpatterns = [
    path('', LoginView.as_view(), name='login'),

    # Dashboards
    path('administrador/dashboard/', DashboardAdminView.as_view(), name='dashboard_admin'),
    path('dashboard-analista/', DashboardAnalistaView.as_view(), name='dashboard_analista'),

    # Admin
    path('administrador/usuarios/', AdminUsuariosView.as_view(), name='admin_usuarios'),

    # API Usuarios
    path('api/usuarios/', UsuarioCRUDView.as_view(), name='usuarios_list_create'),
    path('api/usuarios/<int:usuario_id>/', UsuarioCRUDView.as_view(), name='usuarios_detail'),

    # Pólizas
    path('polizas/', PolizaListView.as_view(), name='polizas_list'),
    path('polizas/<int:pk>/', PolizaDetailView.as_view(), name='poliza_detail'),
    path('polizas/editar/<int:pk>/', PolizaUpdateView.as_view(), name='poliza_update'),
    path('polizas/eliminar/<int:pk>/', PolizaDeleteView.as_view(), name='poliza_delete'),

<<<<<<< HEAD
    # Siniestros
    path('siniestros/', SiniestroListView.as_view(), name='siniestros'),
=======
    # Siniestros (UNA SOLA PANTALLA)
    path('siniestros/', SiniestroListView.as_view(), name='siniestros'),
    # Siniestros
>>>>>>> 023cea205f0f0fa6e2fc75d4401f28287856a05b
    path('siniestros/<int:pk>/', SiniestroDetailView.as_view(), name='siniestro_detail'),
    path('siniestros/<int:pk>/editar/', SiniestroEditView.as_view(), name='siniestro_edit'),
    path('siniestros/<int:pk>/eliminar/', SiniestroDeleteView.as_view(), name='siniestro_delete'),

<<<<<<< HEAD
    # Facturacion
    path('facturas/', lista_facturas, name='lista_facturas'),
    path('facturas/nueva/', crear_factura, name='crear_factura'),
    path('facturas/pdf/<int:factura_id>/', generar_pdf_factura, name='generar_pdf_factura'),

    # Logout
    path('logout/', logout_view, name='logout'),
<<<<<<< Updated upstream
]
=======

    # Logout
    path('logout/', logout_view, name='logout'),
]
>>>>>>> 023cea205f0f0fa6e2fc75d4401f28287856a05b
=======

    # Subida de evidencia para siniestros
    path('siniestros/<int:siniestro_id>/subir-evidencia/', SubirEvidenciaView.as_view(), name='subir_evidencia'),
    path('documentos/<int:pk>/eliminar/', SiniestroDeleteEvidenciaView.as_view(), name='eliminar_evidencia'),

    # GESTIÓN DE CUSTODIOS
    path('custodios/', CustodioListView.as_view(), name='custodios_list'),
    path('custodios/editar/<int:pk>/', CustodioUpdateView.as_view(), name='custodio_update'),
    path('custodios/eliminar/<int:pk>/', CustodioDeleteView.as_view(), name='custodio_delete'),

    # GESTIÓN DE FINIQUITOS
    path('siniestros/<int:siniestro_id>/finiquitar/', FiniquitoCreateView.as_view(), name='crear_finiquito'),

    
    # GESTIÓN DE NOTIFICACIONES
    
    path('notificaciones/', lista_notificaciones, name='lista_notificaciones'),
    path('notificaciones/leer/<int:notificacion_id>/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
]
>>>>>>> Stashed changes
