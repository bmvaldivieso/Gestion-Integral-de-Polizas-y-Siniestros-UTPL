from .models import Usuario

class UsuarioRepository:
    """Repositorio para operaciones de acceso a datos de Usuario"""

    @staticmethod
    def get_by_username(username: str):
        """Buscar usuario por nombre de usuario"""
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

from .models import Usuario, Poliza

class UsuarioRepository:
    # ... (tu código existente de UsuarioRepository) ...
    @staticmethod
    def get_by_username(username: str):
        try:
            return Usuario.objects.get(username=username)
        except Usuario.DoesNotExist:
            return None

# --- AGREGAR ESTO ---
class PolizaRepository:
    """Repositorio para operaciones de acceso a datos de Pólizas"""

    @staticmethod
    def get_all():
        return Poliza.objects.all().order_by('-fecha_registro')

    @staticmethod
    def get_by_id(poliza_id):
        try:
            return Poliza.objects.get(id=poliza_id)
        except Poliza.DoesNotExist:
            return None

    @staticmethod
    def create(data):
        return Poliza.objects.create(**data)

    @staticmethod
    def update(poliza, data):
        for field, value in data.items():
            setattr(poliza, field, value)
        poliza.save()
        return poliza

    @staticmethod
    def delete(poliza):
        poliza.delete()