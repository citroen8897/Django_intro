# Generated by Django 3.2.3 on 2021-05-13 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, default='-', max_length=100, verbose_name='Назва')),
                ('main_file', models.FileField(max_length=500, null=True, upload_to='document/', verbose_name='Головинй файл')),
                ('reg_number', models.CharField(db_index=True, max_length=100, null=True, verbose_name='Реєстраціний номер')),
                ('create_date', models.DateField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата створення документа')),
                ('comment', models.TextField(blank=True, db_index=True, max_length=500, null=True, verbose_name='Короткий зміст')),
            ],
        ),
    ]