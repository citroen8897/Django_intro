# Generated by Django 2.1.2 on 2021-04-12 13:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_tele_magaz', '0005_producttelegramtable_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttelegramtable',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]