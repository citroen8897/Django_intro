# Generated by Django 2.1.2 on 2021-04-11 21:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_tele_magaz', '0002_auto_20210408_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertelegramtable',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
