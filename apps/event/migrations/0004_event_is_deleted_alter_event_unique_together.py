# Generated by Django 4.2.2 on 2023-06-30 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_rename_panitia_ids_event_staffs_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together={('id', 'is_deleted')},
        ),
    ]
