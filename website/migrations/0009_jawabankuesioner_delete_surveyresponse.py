# Generated by Django 5.0.6 on 2024-06-19 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_surveyresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='JawabanKuesioner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jawaban', models.CharField(max_length=255)),
                ('pertanyaan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.kuesioner')),
                ('responden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.responden')),
            ],
        ),
        migrations.DeleteModel(
            name='SurveyResponse',
        ),
    ]
