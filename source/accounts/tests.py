from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        user = User.objects.create_user(username='admin', email='admin@admin.com', password='admin')
        client =  APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
