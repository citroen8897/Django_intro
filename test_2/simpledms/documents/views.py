from .models import Document, Zip
from .serializers import DocumentSerializer, ZipSerializer, ZipCreateSerializer
from rest_framework import viewsets, renderers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from . import travail_methods
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
import datetime
from django.http import FileResponse
import re


def validate(data):
    date_start_valid = re.findall(r"\d{4}-\d{2}-\d{2}", data['date_start'])
    date_fin_valid = re.findall(r"\d{4}-\d{2}-\d{2}", data['date_fin'])
    if not date_start_valid:
        raise ValidationError(['Неверный формат начальной даты!'])
    elif not date_fin_valid:
        raise ValidationError(['Неверный формат конечной даты!'])

    today = datetime.datetime.today().strftime("%Y-%m-%d")
    documents_data_base = Document.objects.filter(create_date__range=[data['date_start'], data['date_fin']])
    if data['date_start'] > data['date_fin']:
        raise ValidationError(['Некорретный временной промежуток!'])
    elif data['date_start'] > today:
        raise ValidationError(['Некорректная начальная дата!'])
    elif documents_data_base.count() == 0:
        raise ValidationError(['В указанном периоде не существует документов!'])


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = {'id': ['in'], 'create_date': ['range']}
    search_fields = ['reg_number']


class PassthroughRenderer(renderers.BaseRenderer):
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class ZipViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ZipSerializer
    queryset = Zip.objects.all()

    @action(detail=False, methods=['post'], serializer_class=ZipCreateSerializer)
    def create_archive(self, request):
        validate(request.data)
        travail_methods.make_new_zip(request)
        return Response('Архив добавлен!')

    @action(methods=['get'], detail=True,
            renderer_classes=(PassthroughRenderer,))
    def download(self, *args, **kwargs):
        instance = self.get_object()
        file_handle = instance.zip_file
        response = FileResponse(file_handle, content_type='application/zip')
        response[
            'Content-Disposition'] = 'attachment; filename="%s"' % instance.title_zip
        return response
