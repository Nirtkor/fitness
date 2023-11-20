from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView
from .views import (
    ClientView,
    TrainerView,
    ClassView,
    MembershipView,
    SubscriptionView,
    IndividualTrainingView,
    main_page,
    calendar_page,
    contact_page,
    lk_page,
    login_view,
    book_session
)

router = DefaultRouter()
router.register('clients', ClientView, basename='clients')
router.register('trainers', TrainerView, basename='trainers')
router.register('classes', ClassView, basename='classes')
router.register('memberships', MembershipView, basename='memberships')
router.register('subscriptions', SubscriptionView, basename='subscriptions')
router.register('individualtrainings', IndividualTrainingView, basename='individualtrainings')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('main/', main_page, name='main-page'),
    path('calendar/', calendar_page, name='calendar-page'),
    path('contacts/', contact_page, name='contact-page'),
    path('lk/', lk_page, name='lk-page'),
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
    path('book_session/', book_session, name='book_session'),
    path('logout/', LogoutView.as_view(next_page="http://127.0.0.1:8000/lk/"), name='logout'),
]