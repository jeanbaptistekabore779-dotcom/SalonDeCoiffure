from django.urls import path
from .views import liste_notifications

urlpatterns = [
    path('', liste_notifications, name='notifications'),
]
