# Generated by Django 5.0.6 on 2024-06-18 06:32

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_responden_tanggal_survey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responden',
            name='tanggal_survey',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]