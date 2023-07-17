from django.urls import reverse


class ReportManager:
    REPORT_URL = reverse('report-list')

    def __init__(self, client):
        self.client = client

    def create_report(self, report_data):
        report_url = reverse('report-list')
        response = self.client.post(report_url, report_data)
        report_id = response.data['id']
        return report_id
