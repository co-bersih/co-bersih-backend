# Generated by Django 4.2.2 on 2023-07-26 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_payment_event_payment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together={('link_id', 'is_deleted')},
        ),
    ]