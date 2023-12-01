from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from fitnessClub.models import IndividualTraining
from fitnessClub.serializers import IndividualTrainingSerializer


class IndividualTrainingViewSetTests(TestCase):

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

    def test_create_individual_training(self):
        data = {
            'user': self.user.id,
            'date': '2023-12-01',
            'time': '12:00:00',
        }
        serializer = IndividualTrainingSerializer(data=data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.post('/individualtrainings/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_individual_training(self):
        individual_training = IndividualTraining.objects.create(
            user=self.user,
            date='2023-12-01',
            time='12:00:00',
        )
        response = self.client.get(f'/individualtrainings/{individual_training.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_individual_training(self):
        individual_training = IndividualTraining.objects.create(
            user=self.user,
            date='2023-12-01',
            time='12:00:00',
        )
        data = {
            'user': self.user.id,
            'date': '2023-12-02',
            'time': '14:00:00',
        }
        serializer = IndividualTrainingSerializer(instance=individual_training, data=data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.put(f'/individualtrainings/{individual_training.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_individual_training(self):
        individual_training = IndividualTraining.objects.create(
            user=self.user,
            date='2023-12-01',
            time='12:00:00',
        )
        data = {
            'time': '14:00:00',
        }
        serializer = IndividualTrainingSerializer(instance=individual_training, data=data, partial=True)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.patch(f'/individualtrainings/{individual_training.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_individual_training(self):
        individual_training = IndividualTraining.objects.create(
            user=self.user,
            date='2023-12-01',
            time='12:00:00',
        )
        response = self.client.delete(f'/individualtrainings/{individual_training.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
