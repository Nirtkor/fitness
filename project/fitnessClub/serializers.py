from rest_framework import serializers
from fitnessClub.models import Client, Trainer, Class, Membership, Subscription, IndividualTraining


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = "__all__"


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class IndividualTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualTraining
        fields = "__all__"
