from django.contrib import admin
from .models import Client, Trainer, Class, Membership, Subscription, IndividualTraining

admin.site.register(Client)
admin.site.register(Trainer)
admin.site.register(Class)
admin.site.register(Membership)
admin.site.register(Subscription)
admin.site.register(IndividualTraining)
