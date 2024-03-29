# Generated by Django 3.2 on 2021-05-15 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_zip', models.CharField(db_index=True, default='-', max_length=100, verbose_name='Назва архiву')),
                ('create_date_zip', models.DateField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата створення архiву')),
                ('quantity_docs', models.CharField(db_index=True, default='-', max_length=15, verbose_name='кiл-ть док-тiв в архiвi')),
                ('link_zip', models.CharField(db_index=True, default='-', max_length=500, verbose_name='Посилання')),
            ],
            options={
                'verbose_name': 'Архiв',
                'verbose_name_plural': 'Архiви',
            },
        ),
    ]
