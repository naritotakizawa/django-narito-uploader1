from rest_framework import viewsets
from .models import Composite
from .serializers import CompositeSerializer


class CompositeViewSet(viewsets.ModelViewSet):
    queryset = Composite.objects.all()
    serializer_class = CompositeSerializer
