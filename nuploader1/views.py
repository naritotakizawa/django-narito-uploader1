import mimetypes
import os
import zipfile
from django.http import FileResponse, HttpResponseNotModified, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.http import http_date
from django.views.static import was_modified_since
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from .models import Composite
from .serializers import CompositeSerializer
from .utils import get_composite, walk_and_write_zip


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


def serve(request, request_path=None):
    if request_path is None or request_path.endswith('/'):
        return render(request, 'nuploader1/index.html')

    composite = get_composite(request_path)
    statobj = os.stat(composite.src.path)
    if not was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(composite.src.path)
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(composite.src.file, content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if encoding:
        response["Content-Encoding"] = encoding
    return response


def download_zip(request, pk):
    composite = get_object_or_404(Composite, pk=pk)
    if not composite.is_dir:
        return HttpResponseBadRequest('ディレクトリではありません。')
    if not composite.zip_depth:
        return HttpResponseBadRequest('ZIPが許可されているディレクトリではありません。')

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{composite.name}.zip"'
    zip_file = zipfile.ZipFile(response, 'w')
    walk_and_write_zip(composite, zip_file, composite.zip_depth)
    return response
