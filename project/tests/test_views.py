from django.test import TestCase
from rest_framework import status
from fitnessClub.models import Client
from django.urls import reverse

EXPECTED_STATUS_CODE = 200


class ClientViewTest(TestCase):
    def setUp(self):
        self.client_instance = Client.objects.create(name='Test Client', address='Test Address', phone='1234567890')

    def test_create_client(self):
        url = reverse('clients-list')
        test_data = {
            'name': 'Test Client',
            'address': 'Test Address',
            'phone': '1234567890',
        }
        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_client(self):
        url = reverse('clients-detail', args=[self.client_instance.client_id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(client_id=self.client_instance.client_id)

    def test_main_page_view(self):
        response = self.client.get(reverse('main-page'))
        self.assertEqual(response.status_code, EXPECTED_STATUS_CODE)

    def test_calendar_page_view_authenticated(self):
        response = self.client.get(reverse('calendar-page'))
        self.assertEqual(response.status_code, EXPECTED_STATUS_CODE)

    def tearDown(self):
        self.client.logout()
