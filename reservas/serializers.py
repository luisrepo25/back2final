from rest_framework import serializers
from .models import Reserva, ReservaServicio, Visitante, ReservaVisitante

class ReservaServicioSerializer(serializers.ModelSerializer):
    # Aquí se manejan los detalles del servicio
    class Meta:
        model = ReservaServicio
        fields = ["id", "servicio", "cantidad", "precio_unitario", "fecha_servicio"]

class ReservaSerializer(serializers.ModelSerializer):
    detalles = ReservaServicioSerializer(many=True)  # Relación de servicios

    class Meta:
        model = Reserva
        fields = ["id", "usuario", "fecha_inicio", "estado", "cupon", "total", "moneda", "detalles", "created_at", "updated_at"]
        read_only_fields = ["estado"]  # Estado solo puede ser modificado por admin o operador

    def create(self, validated_data):
        detalles = validated_data.pop('detalles', [])
        reserva = Reserva.objects.create(**validated_data)  # Creamos la reserva
        # Aquí manejamos la creación de los detalles del servicio
        for detalle in detalles:
            ReservaServicio.objects.create(reserva=reserva, **detalle)
        return reserva

class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = "__all__"

class ReservaVisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservaVisitante
        fields = ["reserva", "visitante", "estado", "es_titular"]
