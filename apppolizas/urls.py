from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginAnalistaView.as_view(), name='login_analista'),
    path('dashboard-analista/', views.DashboardAnalistaView.as_view(), name='dashboard_analista'),
]