from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from fitnessClub.models import Trainer, Client, Class, Subscription
from fitnessClub.serializers import SubscriptionSerializer


class SubscriptionViewSetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            is_superuser=True,
            id=1,
            username='test',
            first_name='test',
            last_name='test',
            password='test',
        )
        token, created = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_subscription(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='Test Phone',
        )
        class_obj = Class.objects.create(
            class_name='Test Class',
            trainer=Trainer.objects.create(
                name='Test Trainer',
                speciality='Test Speciality',
            ),
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        data = {
            'client': client.pk,
            'class_field': class_obj.pk,
            'subscription_date': '2023-12-01',
            # Remove email field
        }
        serializer = SubscriptionSerializer(data=data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.post('/subscriptions/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_subscription(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='Test Phone',
        )
        class_obj = Class.objects.create(
            class_name='Test Class',
            trainer=Trainer.objects.create(
                name='Test Trainer',
                speciality='Test Speciality',
            ),
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        subscription = Subscription.objects.create(
            client=client,
            class_field=class_obj,
            subscription_date='2023-12-01',
        )
        response = self.client.get(f'/subscriptions/{subscription.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_subscription(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='Test Phone',
        )
        class_obj = Class.objects.create(
            class_name='Test Class',
            trainer=Trainer.objects.create(
                name='Test Trainer',
                speciality='Test Speciality',
            ),
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        subscription = Subscription.objects.create(
            client=client,
            class_field=class_obj,
            subscription_date='2023-12-01',
        )
        data = {
            'subscription_date': '2023-12-30',
            # Add other fields you want to update
        }
        serializer = SubscriptionSerializer(instance=subscription, data=data, partial=True)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.patch(f'/subscriptions/{subscription.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_subscription(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='Test Phone',
        )
        class_obj = Class.objects.create(
            class_name='Test Class',
            trainer=Trainer.objects.create(
                name='Test Trainer',
                speciality='Test Speciality',
            ),
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        subscription = Subscription.objects.create(
            client=client,
            class_field=class_obj,
            subscription_date='2023-12-01',
        )
        response = self.client.delete(f'/subscriptions/{subscription.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_subscription(self):
        client = Client.objects.create(
            name='Test Client',
            address='Test Address',
            phone='Test Phone',
        )
        class_obj = Class.objects.create(
            class_name='Test Class',
            trainer=Trainer.objects.create(
                name='Test Trainer',
                speciality='Test Speciality',
            ),
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        subscription = Subscription.objects.create(
            client=client,
            class_field=class_obj,
            subscription_date='2023-12-01',
        )
        data = {
            'client': client.pk,
            'class_field': class_obj.pk,
            'subscription_date': '2023-12-02',
            # Add other fields you want to update
        }
        serializer = SubscriptionSerializer(instance=subscription, data=data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.put(f'/subscriptions/{subscription.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
