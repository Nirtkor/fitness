from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from fitnessClub.models import Trainer, Membership, Client
from fitnessClub.serializers import MembershipSerializer

class MembershipViewSetTests(TestCase):

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

    def test_create_membership(self):
        client = Client.objects.create(
            name='Test Client',
        )
        data = {
            'client': client.pk,
            'start_date': '2023-12-01',
            'end_date': '2023-12-31',
            'cost': 50.0,
        }
        serializer = MembershipSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        response = self.client.post('/memberships/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_membership(self):
        client = Client.objects.create(
            name='Test Client',
        )
        membership = Membership.objects.create(
            client=client,
            start_date='2023-12-01',
            end_date='2023-12-31',
            cost=50.0,
        )
        data = {
            'client': client.pk,
            'start_date': '2023-12-02',
            'end_date': '2023-12-30',
            'cost': 60.0,
        }
        serializer = MembershipSerializer(instance=membership, data=data)
        self.assertTrue(serializer.is_valid())
        response = self.client.put(f'/memberships/{membership.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_membership(self):
        client = Client.objects.create(
            name='Test Client',
        )
        membership = Membership.objects.create(
            client=client,
            start_date='2023-12-01',
            end_date='2023-12-31',
            cost=50.0,
        )
        response = self.client.get(f'/memberships/{membership.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = MembershipSerializer(membership).data
        self.assertEqual(response.data, serialized_data)

    def test_partial_update_membership(self):
        client = Client.objects.create(
            name='Test Client',
        )
        membership = Membership.objects.create(
            client=client,
            start_date='2023-12-01',
            end_date='2023-12-31',
            cost=50.0,
        )
        data = {
            'end_date': '2023-12-30',
        }
        response = self.client.patch(f'/memberships/{membership.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        membership.refresh_from_db()
        self.assertEqual(str(membership.end_date), '2023-12-30')  # Convert date to string for comparison


    def test_delete_membership(self):
        client = Client.objects.create(
            name='Test Client',
        )
        membership = Membership.objects.create(
            client=client,
            start_date='2023-12-01',
            end_date='2023-12-31',
            cost=50.0,
        )
        response = self.client.delete(f'/memberships/{membership.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Membership.DoesNotExist):
            membership.refresh_from_db()