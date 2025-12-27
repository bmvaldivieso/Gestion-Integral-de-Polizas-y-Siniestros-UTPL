from django.urls import path
from .views import (
    LoginAnalistaView, 
    DashboardAnalistaView, 
    PolizaListView,
    PolizaDeleteView,
    PolizaUpdateView
)


urlpatterns = [
    path('', LoginAnalistaView.as_view(), name='login_analista'),
    path('dashboard-analista/', DashboardAnalistaView.as_view(), name='dashboard_analista'),
    
    
    path('polizas/', PolizaListView.as_view(), name='polizas_list'),
    path('polizas/eliminar/<int:pk>/', PolizaDeleteView.as_view(), name='poliza_delete'),
    path('polizas/editar/<int:pk>/', PolizaUpdateView.as_view(), name='poliza_update'),

]