# Generated by Django 4.2.2 on 2023-06-28 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_rename_panitia_ids_event_staffs_and_more'),
        ('user', '0006_user_joined_event_ids'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='joined_event_ids',
        ),
        migrations.AddField(
            model_name='user',
            name='joined_events',
            field=models.ManyToManyField(related_name='joined_users', to='event.event'),
        ),
    ]
