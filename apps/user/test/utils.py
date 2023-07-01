from django.urls import reverse


class UserManager:
    REGISTER_URL = reverse('user-register')
    LOGIN_URL = reverse('user-login')

    def __init__(self, client):
        self.client = client

    def login_user(self, register_data):
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }
        response = self.client.post(self.LOGIN_URL, login_data)
        token = response.data
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token['access'])

    def register_user(self, user_detail):
        response = self.client.post(self.REGISTER_URL, user_detail)
        response.data['password'] = user_detail['password']
        return response.data

    def logout_user(self):
        self.client.credentials()
