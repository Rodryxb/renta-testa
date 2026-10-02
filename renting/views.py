from datetime import timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Maquinaria, Carro, ItemCarro, Contrato, ItemContrato, Usuario
from .serializers import (MaquinariaSerializer, CarroSerializer, ItemCarroSerializer, ContratoSerializer)
from .permissions import IsCliente, IsEjecutivo
from django.contrib.auth.hashers import make_password

# ==============================================================================
# VISTA: REGISTRO DE USUARIOS
# ==============================================================================
class RegistroClienteView(APIView):
    # Cualquier persona en internet puede ver esta ruta (No requiere token)
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        # Validar si el correo ya existe en la base de datos
        if Usuario.objects.filter(username=data.get('email')).exists():
            return Response({"error": "El correo ya está registrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear un usuario nuevo, guardando la clave encriptada (make_password)
        user = Usuario.objects.create(
            username=data.get('email'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            first_name=data.get('nombre', ''),
            telefono=data.get('telefono', ''),
            ciudad=data.get('ciudad', ''),
            rol='CLIENTE' # Se registra como cliente por defecto
        )
        return Response({"mensaje": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)

# ==============================================================================
# VIEWSET: MAQUINARIA Y MATERIALES (CRUD COMPLETO)
# ==============================================================================
# Un ModelViewSet incluye automáticamente las rutas para Listar(GET), Crear(POST),
# Editar(PUT) y Eliminar(DELETE).
class MaquinariaViewSet(viewsets.ModelViewSet):
    queryset = Maquinaria.objects.all().order_by('id')
    # Permite leer datos en formato Multipart (imágenes de la PC) o formato JSON
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = MaquinariaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria', 'tipo'] # Permite filtrar por URL (ej. ?tipo=MATERIAL)

    # Lógica de seguridad: Todo el mundo puede VER (list, retrieve),
    # pero solo los Ejecutivos pueden CREAR, EDITAR o BORRAR.
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsEjecutivo()]

# ==============================================================================
# VISTA: CARRO DE COMPRAS TEMPORAL
# ==============================================================================
class CarroArriendoView(APIView):
    # Tienes que estar logeado para usar el carrito (cualquier rol)
    permission_classes = [permissions.IsAuthenticated]

    # [GET] Traer el carrito del usuario
    def get(self, request):
        # Busca el carrito del usuario. Si no existe, se lo crea vacío automáticamente.
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        return Response(CarroSerializer(carro).data)

    # [POST] Agregar un producto al carrito
    def post(self, request):
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        serializer = ItemCarroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(carro=carro) # Vincula el ítem al carro del usuario
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # [PUT] Editar la cantidad de un material dentro del carro
    def put(self, request):
        item_id = request.data.get('item_id')
        cantidad = request.data.get('cantidad')
        if item_id and cantidad is not None:
            try:
                # Se asegura que el ítem pertenezca al usuario que está consultando
                item = ItemCarro.objects.get(id=item_id, carro__usuario=request.user)
                item.cantidad = int(cantidad)
                item.save()
                return Response({'status': 'actualizado'}, status=status.HTTP_200_OK)
            except ItemCarro.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # [DELETE] Borrar un ítem, o vaciar todo el carrito
    def delete(self, request):
        item_id = request.data.get('item_id')
        if item_id:
            ItemCarro.objects.filter(id=item_id, carro__usuario=request.user).delete()
        else: # Si no manda ID, asume que quiere vaciar el carrito entero
            ItemCarro.objects.filter(carro__usuario=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ==============================================================================
# VISTA: PROCESAMIENTO DE COMPRA FINAL (CHECKOUT)
# ==============================================================================
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # @transaction.atomic asegura que si algo falla (ej. error de internet a la mitad), 
    # la base de datos se echa para atrás y no se descuenta ni un peso ni el stock.
    @transaction.atomic
    def post(self, request):
        carro = Carro.objects.filter(usuario=request.user).first()
        if not carro or not carro.items.exists():
            return Response({"error": "El carro está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Verificar si hay stock real antes de proceder
        for item in carro.items.all():
            if item.maquinaria.stock_disponible < item.cantidad:
                proxima_fecha = ""
                if item.maquinaria.tipo == 'MAQUINARIA':
                    siguiente_devolucion = ItemContrato.objects.filter(
                        maquinaria=item.maquinaria,
                        contrato__estado__in=['PAGADO', 'ENTREGADO']
                    ).order_by('fecha_fin').first()
                    
                    if siguiente_devolucion and siguiente_devolucion.fecha_fin:
                        fecha_disp = siguiente_devolucion.fecha_fin + timedelta(days=1)
                        proxima_fecha = f" Próximo equipo disponible el: {fecha_disp.strftime('%d/%m/%Y')}."
                        
                return Response(
                    {"error": f"Stock insuficiente para {item.maquinaria.nombre}.{proxima_fecha}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 2. Sumar el total y crear la orden (Contrato)
        total_estimado = sum(item.subtotal for item in carro.items.all())
        contrato = Contrato.objects.create(
            usuario=request.user,
            estado='PAGADO',
            total=total_estimado
        )

        # 3. Traspasar los ítems temporales a la orden oficial y descontar stock de bodega
        for item in carro.items.all():
            ItemContrato.objects.create(
                contrato=contrato,
                maquinaria=item.maquinaria,
                fecha_inicio=item.fecha_inicio,
                fecha_fin=item.fecha_fin,
                cantidad=item.cantidad,
                precio_cobrado=item.subtotal # Se guarda el precio histórico
            )
            item.maquinaria.stock_disponible -= item.cantidad
            item.maquinaria.save()

        # 4. Vaciar el carrito temporal
        carro.items.all().delete()
        
        # 5. Retornar el resumen de la orden al Frontend para pintar la boleta
        return Response(ContratoSerializer(contrato).data, status=status.HTTP_201_CREATED)

# ==============================================================================
# VISTAS DE HISTORIAL DE CONTRATOS (ÓRDENES)
# ==============================================================================
class MisContratosView(APIView):
    # Solo el cliente ve sus compras
    permission_classes = [IsCliente]

    def get(self, request):
        contratos = Contrato.objects.filter(usuario=request.user)
        return Response(ContratoSerializer(contratos, many=True).data)

class ContratoEstadoView(APIView):
    # Solo el administrador puede modificar el estado de la entrega
    permission_classes = [IsEjecutivo]

    @transaction.atomic
    def patch(self, request, pk):
        contrato = get_object_or_404(Contrato, pk=pk)
        nuevo_estado = request.data.get('estado')
        estados_validos = dict(Contrato.ESTADOS).keys()

        if nuevo_estado not in estados_validos:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        # Lógica de Stock: Si se cancela la orden o se devuelve la máquina completada,
        # devolver el stock a la bodega.
        if nuevo_estado in ['CANCELADO', 'COMPLETADO'] and contrato.estado not in ['CANCELADO', 'COMPLETADO']:
            for item in contrato.items.all():
                item.maquinaria.stock_disponible += item.cantidad
                item.maquinaria.save()
        
        contrato.estado = nuevo_estado
        contrato.save()
        return Response(ContratoSerializer(contrato).data)


# ==============================================================================
# VIEWSET: ESPECIALISTAS Y TOPÓGRAFOS
# ==============================================================================
from .models import ServicioExterno
from .serializers import ServicioExternoSerializer

class ServicioExternoViewSet(viewsets.ModelViewSet):
    queryset = ServicioExterno.objects.all().order_by('id')
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = ServicioExternoSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsEjecutivo()]


# ==============================================================================
# VISTA: CONFIGURACIÓN DINÁMICA DE LA PÁGINA
# ==============================================================================
from .models import Configuracion
from .serializers import ConfiguracionSerializer

class ConfiguracionView(APIView):
    # Cualquiera puede ver los textos para cargar la página
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        config = Configuracion.get_solo()
        return Response(ConfiguracionSerializer(config).data)
        
    # Solo un ejecutivo puede modificarlos
    def put(self, request):
        if not request.user.is_authenticated or request.user.rol != 'EJECUTIVO':
            return Response(status=status.HTTP_403_FORBIDDEN)
        config = Configuracion.get_solo()
        serializer = ConfiguracionSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DevolucionesActivasView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.utils import timezone
        
        items = ItemContrato.objects.filter(
            contrato__usuario=request.user,
            contrato__estado__in=['PAGADO', 'ENTREGADO'],
            maquinaria__tipo='MAQUINARIA',
            fecha_fin__isnull=False
        ).order_by('fecha_fin')
        
        datos = []
        hoy = timezone.now().date()
        for item in items:
            dias_restantes = (item.fecha_fin - hoy).days
            
            # El dia 0 no cuenta como dijo el usuario (es el día de envío)
            if dias_restantes < 0:
                estado_dias = f"Atrasado por {abs(dias_restantes)} días"
            elif dias_restantes == 0:
                estado_dias = "Día de envío (No cuenta)"
            else:
                estado_dias = f"Quedan {dias_restantes} días"
                
            imagen = ''
            if item.maquinaria.imagen_upload:
                imagen = item.maquinaria.imagen_upload.url
            elif item.maquinaria.imagen_url:
                imagen = item.maquinaria.imagen_url

            datos.append({
                'id': item.id,
                'maquinaria': item.maquinaria.nombre,
                'imagen': imagen,
                'fecha_inicio': item.fecha_inicio.strftime('%d/%m/%Y'),
                'fecha_fin': item.fecha_fin.strftime('%d/%m/%Y'),
                'estado_dias': estado_dias,
                'contrato_id': item.contrato.id
            })
            
        return Response(datos)
