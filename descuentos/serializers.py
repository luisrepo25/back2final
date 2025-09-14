
from rest_framework import serializers
from .models import Descuento, ServicioDescuento
from django.utils import timezone

class DescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Descuento
        fields = "__all__"

class ServicioDescuentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicioDescuento
        fields = "__all__"

    def validate(self, data):
        # Regla anti-solapamiento: no permitir dos descuentos EXCLUSIVOS
        # que se superpongan en el tiempo para el mismo servicio.
        # (chequeo básico con las fechas del Descuento)
        exclusivo = data.get("exclusivo", True)
        servicio = data["servicio"]
        descuento = data["descuento"]
        instance = getattr(self, "instance", None)

        if exclusivo:
            # normaliza ventana del descuento actual
            s1 = descuento.fecha_inicio
            e1 = descuento.fecha_fin

            qs = ServicioDescuento.objects.filter(servicio=servicio, exclusivo=True, estado=True).select_related("descuento")
            if instance:
                qs = qs.exclude(pk=instance.pk)
            for sd in qs:
                d2 = sd.descuento
                s2, e2 = d2.fecha_inicio, d2.fecha_fin

                # Considera None como -∞ / +∞
                s1_eff = s1 or timezone.datetime.min.replace(tzinfo=timezone.utc)
                e1_eff = e1 or timezone.datetime.max.replace(tzinfo=timezone.utc)
                s2_eff = s2 or timezone.datetime.min.replace(tzinfo=timezone.utc)
                e2_eff = e2 or timezone.datetime.max.replace(tzinfo=timezone.utc)

                if s1_eff <= e2_eff and s2_eff <= e1_eff:
                    raise serializers.ValidationError(
                        "Ya existe un descuento EXCLUSIVO que se solapa en fechas para este servicio."
                    )
        return data
