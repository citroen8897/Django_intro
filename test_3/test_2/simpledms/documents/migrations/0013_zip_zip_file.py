# Generated by Django 3.2 on 2021-05-18 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0012_auto_20210517_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='zip',
            name='zip_file',
            field=models.FileField(max_length=500, null=True, upload_to='', verbose_name='Архiв документiв'),
        ),
    ]
