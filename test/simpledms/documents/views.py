from .models import Document, Zip
from .serializers import DocumentSerializer, ZipSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters
from rest_framework.response import Response
import datetime
from . import travail_methods
from django.http import HttpResponse
from wsgiref.util import FileWrapper


class DocumentListCreate(generics.ListCreateAPIView):
    """получить список документов. Добавить новый документ."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class SomeModelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Обращение к конкретному документу по id или reg_number.
    Изменение/Удаление документа."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        pk = self.kwargs[self.lookup_url_kwarg]

        try:
            self.kwargs[self.lookup_url_kwarg] = int(pk)
            self.lookup_field = 'id'
        except:
            self.lookup_field = 'reg_number'

        return super(SomeModelDetailView, self).get_object()


class DocumentsByDateList(generics.ListAPIView):
    """Выборка документов за конкретную дату."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['create_date']


class DocumentFilter(FilterSet):
    """Фильтр по стартовой и конечной дате документа."""

    min_date = filters.DateFilter(field_name="create_date", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="create_date", lookup_expr='lte')

    class Meta:
        model = Document
        fields = ['min_date', 'max_date']


class DocumentListByDateFilter(generics.ListAPIView):
    """Выборка документов за определенный период.
    Проверка наличия хоть одного документа за указанный период.
    Запуск внешних функций для генерации реестров и архивов."""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DocumentFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        quantity_docs = len(queryset)
        if quantity_docs > 0:
            zip_date = datetime.date.today()
            zip_name = zip_date.strftime("%d_%m_%Y")
            new_zip = Zip.objects.create(title_zip=zip_name,
                                         create_date_zip=zip_date,
                                         quantity_docs=quantity_docs)
            last_zip_id = new_zip.id
            zip_link = f'http://127.0.0.1:8000/download/{last_zip_id}'
            travail_methods.zip_list_excel(zip_name, zip_date, quantity_docs,
                                           zip_link)
            Zip.objects.filter(id=last_zip_id).update(link_zip=zip_link)

            travail_methods.make_zip(queryset, zip_name)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ZipListCreate(generics.ListCreateAPIView):
    """Получить список всех архивов.
    Добавление нового архива."""

    queryset = Zip.objects.all()
    serializer_class = ZipSerializer


class SomeModelDetailViewZip(generics.RetrieveUpdateDestroyAPIView):
    """Обращение к конкретному архиву по id или link_zip.
        Изменение/Удаление архива."""

    queryset = Zip.objects.all()
    serializer_class = ZipSerializer
    lookup_url_kwarg = 'pk'

    def get_object(self):
        pk = self.kwargs[self.lookup_url_kwarg]

        try:
            self.kwargs[self.lookup_url_kwarg] = int(pk)
            self.lookup_field = 'id'
        except:
            self.lookup_field = 'link_zip'

        return super(SomeModelDetailViewZip, self).get_object()


class FileDownloadListAPIView(generics.ListAPIView):
    """Отправка Ответа с загрузчиком архива, на запрос с id нужного архива."""

    def get(self, request, id, format=None):
        queryset = Zip.objects.get(id=id)
        file_handle = './static/' + queryset.title_zip + '.zip'
        document = open(file_handle, 'rb')
        response = HttpResponse(FileWrapper(document), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="%s"' % queryset.title_zip
        return response
