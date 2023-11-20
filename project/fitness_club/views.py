from django.shortcuts import render, redirect
from fitnessClub.models import Client, Trainer, Class, Membership, Subscription, IndividualTraining
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from django import forms
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from fitnessClub.serializers import (
    ClientSerializer, TrainerSerializer, ClassSerializer,
    MembershipSerializer, SubscriptionSerializer, IndividualTrainingSerializer,
    )


def client_list(request):
    if request.method == 'POST':
        client = Client(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
        )
        client.save()
        return JsonResponse({'message': 'Client created successfully.'})
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})


def trainer_list(request):
    if request.method == 'POST':
        trainer = Trainer(
            name=request.POST.get('name'),
            speciality=request.POST.get('speciality'),
        )
        trainer.save()
        return JsonResponse({'message': 'Trainer created successfully.'})
    trainers = Trainer.objects.all()
    return render(request, 'trainer_list.html', {'trainers': trainers})


def class_list(request):
    if request.method == 'POST':
        class_instance = Class(
            class_name=request.POST.get('class_name'),
            trainer_id=request.POST.get('trainer_id'),
            class_date=request.POST.get('class_date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
        )
        class_instance.save()
        return JsonResponse({'message': 'Class created successfully.'})
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})


def membership_list(request):
    if request.method == 'POST':
        membership = Membership(
            client_id=request.POST.get('client_id'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            cost=request.POST.get('cost'),
        )
        membership.save()
        return JsonResponse({'message': 'Membership created successfully.'})
    memberships = Membership.objects.all()
    return render(request, 'membership_list.html', {'memberships': memberships})


def subscription_list(request):
    if request.method == 'POST':
        subscription = Subscription(
            client_id=request.POST.get('client_id'),
            class_id=request.POST.get('class_id'),
            subscription_date=request.POST.get('subscription_date'),
        )
        subscription.save()
        return JsonResponse({'message': 'Subscription created successfully.'})
    subscriptions = Subscription.objects.all()
    return render(request, 'subscription_list.html', {'subscriptions': subscriptions})


def main_page(request):
    return render(request, 'index.html')


def calendar_page(request):
    if request.user.is_authenticated:
        return render(request, 'calendar.html')
    return login_view(request)


def contact_page(request):
    return render(request, 'contacts.html')


def lk_page(request):
    if request.user.is_authenticated:
        return render(request, 'lk.html')
    return login_view(request)


class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/lk/")
            else:
                messages.error(request, "Неправильный логин или пароль")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def book_session(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            date = request.POST['day']
            time = request.POST['time']

            existing_sessions = IndividualTraining.objects.filter(user=user, date=date, time=time)

            if existing_sessions.exists():
                data_msg = {
                    'message': 'У вас уже есть запись на эту дату и время',
                }
                return render(request, 'calendar.html', data_msg)
            else:
                new_session = IndividualTraining(user=user, date=date, time=time)
                new_session.save()
                data_msg = {
                    'message': 'Вы успешно записались!',
                }
                return render(request, 'calendar.html', data_msg)
    else:
        return render(request, 'login.html')


class ClientView(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class TrainerView(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer


class ClassView(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class MembershipView(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class SubscriptionView(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class IndividualTrainingView(viewsets.ModelViewSet):
    queryset = IndividualTraining.objects.all()
    serializer_class = IndividualTrainingSerializer


@method_decorator(csrf_exempt, name='dispatch')
class IndividualTrainingDeleteView(View):
    def delete(self, request, *args, **kwargs):
        training = get_object_or_404(IndividualTraining, id=self.kwargs['pk'])
        training.delete()
        return JsonResponse({'status': 'success'})
