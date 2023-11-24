from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APIClient
from fitnessClub.models import Trainer, Class
from fitnessClub.serializers import ClassSerializer


class ClassViewSetTests(TestCase):

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

    def test_create_class(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        data = {
            'class_name': 'Test Class',
            'trainer': trainer.pk,  # Use the trainer instance instead of trainer_id
            'class_date': '2023-12-01',
            'start_time': '10:00:00',
            'end_time': '12:00:00',
        }
        serializer = ClassSerializer(data=data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.post('/classes/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_class(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        class_instance = Class.objects.create(
            class_name='Test Class',
            trainer=trainer,
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        response = self.client.get(f'/classes/{class_instance.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_class(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        class_instance = Class.objects.create(
            class_name='Test Class',
            trainer=trainer,
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        data = {
            'class_name': 'Updated Class',
            'trainer': trainer.pk,  # Use the trainer instance instead of trainer_id
            'class_date': '2023-12-02',
            'start_time': '14:00:00',
            'end_time': '16:00:00',
        }
        serializer = ClassSerializer(instance=class_instance, data=data)
        if not serializer.is_valid():
            print(f"Validation errors: {serializer.errors}")
        self.assertTrue(serializer.is_valid())
        response = self.client.put(f'/classes/{class_instance.pk}/', data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_class(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        class_instance = Class.objects.create(
            class_name='Test Class',
            trainer=trainer,
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        data = {
            'class_name': 'Updated Class',
        }
        response = self.client.patch(f'/classes/{class_instance.pk}/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_class(self):
        trainer = Trainer.objects.create(
            name='Test Trainer',
            speciality='Test Speciality',
        )
        class_instance = Class.objects.create(
            class_name='Test Class',
            trainer=trainer,
            class_date='2023-12-01',
            start_time='10:00:00',
            end_time='12:00:00',
        )
        response = self.client.delete(f'/classes/{class_instance.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Class.objects.filter(pk=class_instance.pk).exists())
