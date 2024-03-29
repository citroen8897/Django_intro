# Generated by Django 3.2 on 2021-05-17 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0009_delete_docsinzip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zip',
            name='date_fin',
            field=models.DateField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата завершення вибiрки YYYY-MM-DD'),
        ),
        migrations.AlterField(
            model_name='zip',
            name='date_start',
            field=models.DateField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата початку вибiрки YYYY-MM-DD'),
        ),
    ]
