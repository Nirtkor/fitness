from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from fitnessClub.models import Trainer


class TrainerViewSetTests(TestCase):

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

    def test_create_trainer(self):
        data = {
            'name': 'Test Trainer',
            'speciality': 'Test Speciality',
        }
        response = self.client.post('/trainers/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_trainer(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        response = self.client.get(f'/trainers/{trainer.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_trainer(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        data = {
            'name': 'Updated Trainer',
            'speciality': 'Updated Speciality',
        }
        response = self.client.put(f'/trainers/{trainer.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_trainer(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        data = {
            'speciality': 'Updated Speciality',
        }
        response = self.client.patch(f'/trainers/{trainer.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_trainer(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        response = self.client.delete(f'/trainers/{trainer.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Trainer.objects.filter(pk=trainer.pk).exists())
