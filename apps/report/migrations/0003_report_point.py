# Generated by Django 4.2.2 on 2023-07-06 06:57

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_report_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]