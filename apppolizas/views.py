from django.views.generic import FormView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .forms import LoginForm
from .services import AuthService
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from .forms import PolizaForm
from .services import PolizaService


class LoginAnalistaView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request, *args, **kwargs):
        """
        Sobrescribimos el POST para responder con JSON para el manejo de JWT
        """
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # Llamada al Servicio
                token = AuthService.login_analista(username, password)
                
                # Respuesta Exitosa con Token
                return JsonResponse({
                    'success': True,
                    'token': token,
                    'message': 'Inicio de sesión exitoso'
                }, status=200)

            except ValidationError as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=403)
        
        return JsonResponse({'success': False, 'error': 'Datos de formulario inválidos'}, status=400)



class DashboardAnalistaView(TemplateView):
    template_name = 'dashboard.html'        

class PolizaListView(View):
    template_name = 'polizas.html'

    def get(self, request, *args, **kwargs):
        polizas = PolizaService.listar_polizas()
        form = PolizaForm() # Formulario vacío para el modal de crear
        return render(request, self.template_name, {'polizas': polizas, 'form': form})

    def post(self, request, *args, **kwargs):
        # Opción para CREAR desde la misma página (modal)
        form = PolizaForm(request.POST)
        if form.is_valid():
            try:
                PolizaService.crear_poliza(form.cleaned_data)
                messages.success(request, 'Póliza creada exitosamente')
                return redirect('polizas_list')
            except Exception as e:
                messages.error(request, f'Error al crear: {str(e)}')
        
        polizas = PolizaService.listar_polizas()
        return render(request, self.template_name, {'polizas': polizas, 'form': form})

class PolizaUpdateView(View):
    template_name = 'poliza_edit.html'
    
    def post(self, request, pk, *args, **kwargs):
        template_name = 'poliza_edit.html' # Usaremos un template específico para editar

    def get(self, request, pk, *args, **kwargs):
        try:
            poliza = PolizaService.obtener_poliza(pk)
            form = PolizaForm(instance=poliza) # Carga los datos existentes en el form
            return render(request, self.template_name, {'form': form, 'poliza': poliza})
        except Exception as e:
            messages.error(request, 'Error al cargar la póliza')
            return redirect('polizas_list')

    def post(self, request, pk, *args, **kwargs):
        try:
            poliza = PolizaService.obtener_poliza(pk)
            form = PolizaForm(request.POST, instance=poliza)
            
            if form.is_valid():
                # Pasamos los datos limpios al servicio para que actualice
                PolizaService.actualizar_poliza(pk, form.cleaned_data)
                messages.success(request, 'Póliza actualizada exitosamente')
                return redirect('polizas_list')
            else:
                messages.error(request, 'Por favor corrige los errores del formulario')
        
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
            
        return render(request, self.template_name, {'form': form, 'poliza': poliza})

class PolizaDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            PolizaService.eliminar_poliza(pk)
            messages.success(request, 'Póliza eliminada')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        return redirect('polizas_list')