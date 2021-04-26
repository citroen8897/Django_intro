# Generated by Django 3.2 on 2021-04-25 20:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=75)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=75)),
                ('nom', models.CharField(max_length=100)),
                ('etre', models.CharField(max_length=25)),
                ('quantity', models.CharField(max_length=35)),
                ('prix', models.FloatField()),
                ('img', models.CharField(max_length=25)),
                ('author', models.CharField(max_length=75)),
                ('published_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='nom',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='prenom',
            field=models.CharField(max_length=50),
        ),
    ]
