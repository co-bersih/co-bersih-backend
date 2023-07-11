from apps.user.models import User
from apps.user.serializers import UserSerializer
from django.urls import reverse


class UserManager:
    REGISTER_URL = reverse('user-register')
    LOGIN_URL = reverse('user-login')
    DEFAULT_ADMIN_DETAIL = {
        'email': 'admin@mail.com',
        'password': 'admin',
        'name': 'admin',
    }

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

    def create_admin(self, admin_detail=None):
        admin_detail = admin_detail or self.DEFAULT_ADMIN_DETAIL
        admin = User.objects.create_superuser(**admin_detail)

        serializer = UserSerializer(admin)
        data = serializer.data
        data['password'] = admin_detail['password']
        data['is_admin'] = admin.is_admin
        data['is_staff'] = admin.is_staff
        data['is_superuser'] = admin.is_superuser

        return data
