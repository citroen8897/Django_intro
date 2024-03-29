# Generated by Django 3.2 on 2021-05-17 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_zip'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocsInZip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_numero', models.IntegerField(db_index=True, default='-', max_length=15, verbose_name='Zip_Id')),
                ('doc_numero', models.IntegerField(db_index=True, default='-', max_length=15, verbose_name='Doc_Id')),
            ],
        ),
        migrations.AlterField(
            model_name='zip',
            name='quantity_docs',
            field=models.IntegerField(db_index=True, default='-', max_length=15, verbose_name='кiл-ть док-тiв в архiвi'),
        ),
    ]
