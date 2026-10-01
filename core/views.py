from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')

def auth_view(request):
    return render(request, 'auth.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')

def maquinas_view(request):
    context = {
        'tipo': 'MAQUINARIA',
        'titulo': 'Catálogo de Maquinarias',
        'subtitulo': 'Cotiza y reserva arriendos de maquinaria pesada. Precios sujetos a factores de uso y flete.'
    }
    return render(request, 'catalogo.html', context)

def materiales_view(request):
    context = {
        'tipo': 'MATERIAL',
        'titulo': 'Venta de Materiales en Stock',
        'subtitulo': 'Compra directa de materiales de construcción. ¡Descuento automático del 10% llevando 30 unidades o más!'
    }
    return render(request, 'catalogo.html', context)


def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def otros_servicios_view(request):
    return render(request, 'servicios.html')

from django.shortcuts import get_object_or_404

def producto_detalle_view(request, pk):
    from renting.models import Maquinaria
    producto = get_object_or_404(Maquinaria, pk=pk)
    return render(request, 'producto_detalle.html', {'producto': producto})


def carro_view(request):
    return render(request, 'carro.html')
