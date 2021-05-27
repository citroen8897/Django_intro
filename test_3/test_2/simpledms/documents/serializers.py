from rest_framework import serializers
from .models import Document, Zip


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'main_file', 'reg_number', 'create_date', 'comment')


class ZipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zip
        fields = ('id', 'title_zip', 'create_date_zip', 'quantity_docs', 'link_zip')


class ZipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zip
        fields = ('date_start', 'date_fin')
