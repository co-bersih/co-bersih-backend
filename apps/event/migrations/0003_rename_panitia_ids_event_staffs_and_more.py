# Generated by Django 4.2.2 on 2023-06-28 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_rename_host_id_event_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='panitia_ids',
            new_name='staffs',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='support_ids',
            new_name='supports',
        ),
    ]