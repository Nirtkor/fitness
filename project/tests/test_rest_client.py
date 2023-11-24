from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from fitnessClub.models import Client
from fitnessClub.serializers import ClientSerializer


class ClientViewSetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            email='test@mail.ru',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_client(self):
        data = {
            'name': 'Test Client',
            'address': 'Test Address',
            'phone': '1234567890'
        }
        response = self.client.post('/clients/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_client(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='1234567890'
        )
        response = self.client.get(f'/clients/{client.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# кто эти тесты выдумал, это же просто жесть

    def test_update_client(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='1234567890'
        )
        data = {
            'name': 'Updated Client',
            'address': 'Updated Address',
            'phone': '9876543210'
        }
        response = self.client.put(f'/clients/{client.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_client(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='1234567890'
        )
        data = {
            'address': 'Updated Address',
        }
        response = self.client.patch(f'/clients/{client.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_client(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='1234567890'
        )
        response = self.client.delete(f'/clients/{client.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(pk=client.pk).exists())
