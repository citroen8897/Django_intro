from .models import Document
from .serializers import DocumentSerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet, filters


class DocumentListCreate(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class SomeModelDetailView(generics.RetrieveUpdateDestroyAPIView):
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
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['create_date']


class DocumentFilter(FilterSet):
    min_date = filters.DateFilter(field_name="create_date", lookup_expr='gte')
    max_date = filters.DateFilter(field_name="create_date", lookup_expr='lte')

    class Meta:
        model = Document
        fields = ['min_date', 'max_date']


class DocumentListByDateFilter(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DocumentFilter
