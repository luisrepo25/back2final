from rest_framework import serializers
from .models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"  # expone todos los campos del modelo

from .models import Destino

class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = "__all__"  # expone todos los campos del modelo

from .models import Itinerario

class ItinerarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerario
        fields = "__all__"  # expone todos los campos del modelo

from .models import Paquete
from .serializers import CategoriaSerializer, DestinoSerializer, ItinerarioSerializer

class PaqueteSerializer(serializers.ModelSerializer):
    # Relacionar la categoría (solo mostramos el nombre)
    categoria = CategoriaSerializer(read_only=True)  # Mostrar categoría completa, no solo el id
    # Relacionar destinos
    destinos = DestinoSerializer(many=True, read_only=True)  # Destinos asociados al paquete
    # Relacionar itinerarios
    itinerario = ItinerarioSerializer(many=True, read_only=True)  # Itinerarios asociados al paquete
    
    class Meta:
        model = Paquete
        fields = "__all__"  # expone todos los campos del modelo

from rest_framework import viewsets
from .models import Paquete
from .serializers import PaqueteSerializer

class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquete.objects.all()
    serializer_class = PaqueteSerializer
