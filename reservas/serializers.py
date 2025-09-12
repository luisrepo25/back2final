
from rest_framework import serializers
from .models import Reserva, ReservaServicio, Visitante, ReservaVisitante
from authz.models import Usuario
from catalogo.models import Servicio

class ReservaServicioSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source="servicio.tipo", read_only=True)
    titulo = serializers.CharField(source="servicio.titulo", read_only=True)
    class Meta:
        model = ReservaServicio
        fields = ["servicio", "tipo", "titulo", "cantidad", "precio_unitario", "fecha_servicio"]

class UsuarioReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["id", "nombres", "apellidos", "email", "telefono"]

class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = ["id", "nombre", "apellido", "documento", "fecha_nacimiento", "nacionalidad", "email", "telefono"]

class ReservaVisitanteSerializer(serializers.ModelSerializer):
    visitante = VisitanteSerializer()
    class Meta:
        model = ReservaVisitante
        fields = ["visitante", "estado", "es_titular"]

class ReservaSerializer(serializers.ModelSerializer):
    usuario = UsuarioReservaSerializer(read_only=True)
    detalles = ReservaServicioSerializer(many=True, read_only=True)
    visitantes = ReservaVisitanteSerializer(many=True, read_only=True)
    class Meta:
        model = Reserva
        fields = [
            "id", "usuario", "fecha_inicio", "estado", "cupon", "total", "moneda", "detalles", "visitantes", "created_at", "updated_at"
        ]
        read_only_fields = ["estado", "usuario"]

    def create(self, validated_data):
        detalles = validated_data.pop('detalles', [])
        reserva = Reserva.objects.create(**validated_data)  # Creamos la reserva
        # Aquí manejamos la creación de los detalles del servicio
        for detalle in detalles:
            ReservaServicio.objects.create(reserva=reserva, **detalle)
        return reserva
