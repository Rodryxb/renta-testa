from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Maquinaria, Carro, ItemCarro, Contrato, ItemContrato

from datetime import timedelta

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['rol'] = user.rol
        
        # Lógica de seguridad: Diferenciar tiempo de expiración según el rol
        if user.rol == 'EJECUTIVO':
            token.set_exp(lifetime=timedelta(minutes=2)) # Superusuarios: 2 min
        else:
            token.set_exp(lifetime=timedelta(hours=24)) # Clientes: 24 hrs
            
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['rol'] = self.user.rol
        data['first_name'] = self.user.first_name or self.user.username.split('@')[0]
        data['email'] = self.user.email
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MaquinariaSerializer(serializers.ModelSerializer):
    imagen_final = serializers.SerializerMethodField()

    class Meta:
        model = Maquinaria
        fields = '__all__'

    def get_imagen_final(self, obj):
        if obj.imagen_upload:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen_upload.url)
            return obj.imagen_upload.url
        return obj.imagen_url

class ItemCarroSerializer(serializers.ModelSerializer):
    dias = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    maquinaria_detalle = MaquinariaSerializer(source='maquinaria', read_only=True)
    
    class Meta:
        model = ItemCarro
        fields = ['id', 'maquinaria', 'maquinaria_detalle', 'fecha_inicio', 'fecha_fin', 'cantidad', 'factor_uso', 'costo_delivery', 'dias', 'subtotal']

class CarroSerializer(serializers.ModelSerializer):
    items = ItemCarroSerializer(many=True, read_only=True)
    total_estimado = serializers.SerializerMethodField()

    class Meta:
        model = Carro
        fields = ['id', 'usuario', 'items', 'total_estimado']

    def get_total_estimado(self, obj):
        return sum(item.subtotal for item in obj.items.all())

class ItemContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemContrato
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):
    items = ItemContratoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Contrato
        fields = '__all__'


from .models import ServicioExterno
class ServicioExternoSerializer(serializers.ModelSerializer):
    foto_final = serializers.SerializerMethodField()

    class Meta:
        model = ServicioExterno
        fields = '__all__'

    def get_foto_final(self, obj):
        if obj.foto_upload:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_upload.url)
            return obj.foto_upload.url
        return obj.foto_url


from .models import Configuracion
class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = '__all__'
