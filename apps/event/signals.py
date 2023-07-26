import requests
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Event
from .serializers import PaymentSerializer


@receiver(pre_save, sender=Event)
def set_payment_field(sender, instance, **kwargs):
    if instance.payment:
        return

    bill = create_bill(instance)
    print(bill)

    # Create payment
    serializer = PaymentSerializer(data=bill)
    serializer.is_valid(raise_exception=True)
    payment = serializer.save()

    instance.payment = payment


def create_bill(instance):
    create_bill_url = f'{settings.FLIP_BASE_URL}/pwf/bill'
    payload = {
        'title': instance.id,
        'type': 'MULTIPLE',
        'step': 1,
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", create_bill_url, headers=headers, data=payload,
                                auth=(f'{settings.FLIP_API_SECRET_KEY}:', ''))
    bill = response.json()
    return bill
