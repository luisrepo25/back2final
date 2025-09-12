from rest_framework import viewsets
from .models import Categoria
from .serializers import CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()  # Obtener todas las categorías
    serializer_class = CategoriaSerializer  # Serializador a usar

from rest_framework import viewsets
from .models import Destino
from .serializers import DestinoSerializer

class DestinoViewSet(viewsets.ModelViewSet):
    queryset = Destino.objects.all()  # Obtener todos los destinos
    serializer_class = DestinoSerializer  # Serializador a usar

from rest_framework import viewsets
from .models import Itinerario
from .serializers import ItinerarioSerializer

class ItinerarioViewSet(viewsets.ModelViewSet):
    queryset = Itinerario.objects.all()  # Obtener todos los itinerarios
    serializer_class = ItinerarioSerializer  # Serializador a usar

from rest_framework import viewsets
from .models import Paquete
from .serializers import PaqueteSerializer

class PaqueteViewSet(viewsets.ModelViewSet):
    queryset = Paquete.objects.all()  # Obtener todos los paquetes
    serializer_class = PaqueteSerializer  # Serializador a usar
