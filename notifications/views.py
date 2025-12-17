from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def liste_notifications(request):
    notifications = Notification.objects.filter(
        utilisateur=request.user
    ).order_by('-date')

    return render(request, 'notifications/liste.html', {
        'notifications': notifications
    })
