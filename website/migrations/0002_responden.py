# Generated by Django 5.0.6 on 2024-06-17 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=255)),
                ('jenis_kelamin', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('no_telepon', models.CharField(max_length=20)),
                ('nopol_kendaraan', models.CharField(max_length=20)),
                ('medsos', models.CharField(max_length=255)),
                ('uptd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.subunit')),
            ],
        ),
    ]