# Generated by Django 4.2.2 on 2023-07-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_alter_event_staffs'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
