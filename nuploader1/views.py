import zipfile
from django.http import FileResponse, HttpResponseBadRequest, HttpResponse
from django.utils.cache import patch_response_headers
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from .models import Composite
from .serializers import CompositeSerializer
from .utils import get_composite, walk_and_write


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


def top(request, request_path=None):
    if request_path is not None and not request_path.endswith('/'):
        composite = get_composite(request_path)
        if not composite.is_dir:
            response = FileResponse(composite.src.file)
            patch_response_headers(response)  # whitenoiseとか参考に
            return response
    return render(request, 'nuploader1/index.html')


def download_zip(request, pk):
    composite = get_object_or_404(Composite, pk=pk)
    if not composite.is_dir:
        return HttpResponseBadRequest('ディレクトリではありません。')
    if not composite.zip_depth:
        return HttpResponseBadRequest('ZIPが許可されているディレクトリではありません。')

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{composite.name}.zip"'
    zip_file = zipfile.ZipFile(response, 'w')
    walk_and_write(composite, zip_file, composite.zip_depth)
    return response
