from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Categoria

@receiver(post_migrate)
def cargar_categorias(sender=None, **kwargs):
    # Solo ejecuta esta función después de la migración de la app roomApp
    if sender and sender.name == 'roomApp':
        # Define los datos de las categorías
        categorias_data = [
            {
                'nombre': 'Estados Unidos',
                'descripcion': 'Hoteles de lujo y vip',
                'foto': 'img/chile.jpg',
            },
            {
                'nombre': 'Mexico',
                'descripcion': 'Hoteles estilo viejo oeste!',
                'foto': 'categorias/ropa.jpg',
            },
            {
                'nombre': 'Chile',
                'descripcion': 'Hoteles modernos y elegantes',
                'foto': 'categorias/hogar.jpg',
            },
        ]

        # Elimina todas las categorías existentes
        Categoria.objects.all().delete()

        # Crea las nuevas categorías
        for categoria_data in categorias_data:
            Categoria.objects.create(**categoria_data)
