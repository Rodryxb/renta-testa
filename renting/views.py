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

class RegistroClienteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        if Usuario.objects.filter(username=data.get('email')).exists():
            return Response({"error": "El correo ya está registrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = Usuario.objects.create(
            username=data.get('email'),
            email=data.get('email'),
            password=make_password(data.get('password')),
            first_name=data.get('nombre', ''),
            telefono=data.get('telefono', ''),
            ciudad=data.get('ciudad', ''),
            rol='CLIENTE'
        )
        return Response({"mensaje": "Usuario registrado exitosamente"}, status=status.HTTP_201_CREATED)

class MaquinariaViewSet(viewsets.ModelViewSet):
    queryset = Maquinaria.objects.all().order_by('id')
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = MaquinariaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria', 'tipo']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsEjecutivo()]

class CarroArriendoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        return Response(CarroSerializer(carro).data)

    def post(self, request):
        carro, _ = Carro.objects.get_or_create(usuario=request.user)
        serializer = ItemCarroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(carro=carro)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        item_id = request.data.get('item_id')
        cantidad = request.data.get('cantidad')
        if item_id and cantidad is not None:
            try:
                item = ItemCarro.objects.get(id=item_id, carro__usuario=request.user)
                item.cantidad = int(cantidad)
                item.save()
                return Response({'status': 'actualizado'}, status=status.HTTP_200_OK)
            except ItemCarro.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        item_id = request.data.get('item_id')
        if item_id:
            ItemCarro.objects.filter(id=item_id, carro__usuario=request.user).delete()
        else:
            ItemCarro.objects.filter(carro__usuario=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckoutView(APIView):
    permission_classes = [IsCliente]

    @transaction.atomic
    def post(self, request):
        carro = Carro.objects.filter(usuario=request.user).first()
        if not carro or not carro.items.exists():
            return Response({"error": "El carro está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        for item in carro.items.all():
            if item.maquinaria.stock_disponible < item.cantidad:
                return Response(
                    {"error": f"Stock insuficiente para {item.maquinaria.nombre}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        total_estimado = sum(item.subtotal for item in carro.items.all())
        contrato = Contrato.objects.create(
            usuario=request.user,
            estado='PAGADO',
            total=total_estimado
        )

        for item in carro.items.all():
            ItemContrato.objects.create(
                contrato=contrato,
                maquinaria=item.maquinaria,
                fecha_inicio=item.fecha_inicio,
                fecha_fin=item.fecha_fin,
                cantidad=item.cantidad,
                precio_cobrado=item.subtotal
            )
            item.maquinaria.stock_disponible -= item.cantidad
            item.maquinaria.save()

        carro.items.all().delete()
        return Response(ContratoSerializer(contrato).data, status=status.HTTP_201_CREATED)

class MisContratosView(APIView):
    permission_classes = [IsCliente]

    def get(self, request):
        contratos = Contrato.objects.filter(usuario=request.user)
        return Response(ContratoSerializer(contratos, many=True).data)

class ContratoEstadoView(APIView):
    permission_classes = [IsEjecutivo]

    @transaction.atomic
    def patch(self, request, pk):
        contrato = get_object_or_404(Contrato, pk=pk)
        nuevo_estado = request.data.get('estado')
        estados_validos = dict(Contrato.ESTADOS).keys()

        if nuevo_estado not in estados_validos:
            return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if nuevo_estado in ['CANCELADO', 'COMPLETADO'] and contrato.estado not in ['CANCELADO', 'COMPLETADO']:
            for item in contrato.items.all():
                item.maquinaria.stock_disponible += item.cantidad
                item.maquinaria.save()
        
        elif nuevo_estado == 'PAGADO' and contrato.estado == 'PENDIENTE':
            for item in contrato.items.all():
                if item.maquinaria.stock_disponible < item.cantidad:
                    return Response({"error": f"Sin stock de {item.maquinaria.nombre}"}, status=400)
                item.maquinaria.stock_disponible -= item.cantidad
                item.maquinaria.save()

        contrato.estado = nuevo_estado
        contrato.save()
        return Response(ContratoSerializer(contrato).data)


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


from .models import Configuracion
from .serializers import ConfiguracionSerializer

class ConfiguracionView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        config = Configuracion.get_solo()
        return Response(ConfiguracionSerializer(config).data)
        
    def put(self, request):
        if not request.user.is_authenticated or request.user.rol != 'EJECUTIVO':
            return Response(status=status.HTTP_403_FORBIDDEN)
        config = Configuracion.get_solo()
        serializer = ConfiguracionSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
