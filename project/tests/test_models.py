# ваше_приложение/tests/test_models.py

from django.test import TestCase
from fitnessClub.models import Client, Trainer, Class, Membership, Subscription, IndividualTraining
from django.contrib.auth import get_user_model

class ModelsTest(TestCase):
    def setUp(self):
        self.user, _ = get_user_model().objects.get_or_create(username='testuser', 
                                                              defaults={'password': 'testpassword'},
                                                              )

    def test_client_model(self):
        client = Client.objects.create(name='Test Client', address='Test Address', phone='1234567890')
        self.assertEqual(client.name, 'Test Client')
        self.assertEqual(client.address, 'Test Address')
        self.assertEqual(client.phone, '1234567890')

    def test_trainer_model(self):
        trainer = Trainer.objects.create(name='Test Trainer', speciality='Test Speciality')
        self.assertEqual(trainer.name, 'Test Trainer')
        self.assertEqual(trainer.speciality, 'Test Speciality')

    def test_class_model(self):
        trainer = Trainer.objects.create(name='Test Trainer', speciality='Test Speciality')
        class_instance = Class.objects.create(class_name='Test Class', 
                                              trainer=trainer, 
                                              class_date='2023-01-01', 
                                              start_time='12:00:00', 
                                              end_time='13:00:00',
                                              )
        self.assertEqual(class_instance.class_name, 'Test Class')
        self.assertEqual(class_instance.trainer, trainer)

    def test_membership_model(self):
        client = Client.objects.create(name='Test Client', address='Test Address', phone='1234567890')
        membership = Membership.objects.create(client=client, 
                                               start_date='2023-01-01', 
                                               end_date='2023-12-31', 
                                               cost=100,
                                               )
        self.assertEqual(membership.client, client)
        self.assertEqual(membership.cost, 100.00)

    def test_subscription_model(self):
        client = Client.objects.create(name='Test Client', address='Test Address', phone='1234567890')
        trainer = Trainer.objects.create(name='Test Trainer', speciality='Test Speciality')
        class_instance = Class.objects.create(class_name='Test Class', 
                                              trainer=trainer, 
                                              class_date='2023-01-01', 
                                              start_time='12:00:00', 
                                              end_time='13:00:00',
                                              )
        subscription = Subscription.objects.create(client=client, 
                                                   class_field=class_instance, 
                                                   subscription_date='2023-01-01',
                                                   )
        self.assertEqual(subscription.client, client)
        self.assertEqual(subscription.class_field, class_instance)

    def test_individual_training_model(self):
        training = IndividualTraining.objects.create(user=self.user, date='2023-01-01', time='12:00:00')
        self.assertEqual(training.user, self.user)
        self.assertEqual(training.date, '2023-01-01')
        self.assertEqual(training.time, '12:00:00')
