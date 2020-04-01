from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from .models import Composite
from .serializers import CompositeSerializer
from .utils import get_composite


class CompositeViewSet(viewsets.ModelViewSet):
    queryset = Composite.objects.all()
    serializer_class = CompositeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Composite.objects.filter(parent__isnull=True)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetCompositeFromPath(generics.RetrieveAPIView):
    queryset = Composite.objects.all()
    serializer_class = CompositeSerializer

    def get_object(self):
        request_path = self.kwargs['request_path']
        composite = get_composite(request_path)
        return composite
