from apps.event.models import Event
from django.urls import reverse


class EventManager:
    EVENT_LIST_URL = reverse('event-list')

    def __init__(self, client):
        self.client = client

    def create_event(self, created_event_data):
        response = self.client.post(self.EVENT_LIST_URL, created_event_data)
        return response.data['id']

    def join_event(self, event_id):
        join_event_url = reverse('event-join', kwargs={'pk': event_id})
        response = self.client.post(join_event_url)
        return response

    def create_events(self, total_event, created_event_data):
        event_ids = []

        for i in range(total_event):
            created_event_data['name'] = f'{created_event_data["name"]}{i}'
            event_id = self.create_event(created_event_data)
            event_ids.append(event_id)

        return event_ids

    def join_events(self, event_ids):
        for event_id in event_ids:
            self.join_event(event_id)

    def verify_event(self, event_id):
        event = Event.objects.get(pk=event_id)
        event.is_verified = True
        event.save()

    def verify_events(self, event_ids):
        for event_id in event_ids:
            event = Event.objects.get(pk=event_id)
            event.is_verified = True
            event.save()

    def unverify_event(self, event_id):
        event = Event.objects.get(pk=event_id)
        event.is_verified = False
        event.save()

    def add_staff(self, event_id, staff_email):
        update_staff_event_url = reverse('event-staff-list', kwargs={'pk': event_id})
        self.client.post(update_staff_event_url, {'staff_email': staff_email})
