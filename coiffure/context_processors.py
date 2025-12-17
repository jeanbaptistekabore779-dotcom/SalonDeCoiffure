from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        user_notifications = Notification.objects.filter(utilisateur=request.user)
        notifs_non_lues = user_notifications.filter(lu=False).count()
        notifications_recents = user_notifications.order_by('-date')[:5]
    else:
        notifications_recents = []
        notifs_non_lues = 0

    return {
        'notifications': notifications_recents,
        'notif_count': notifs_non_lues,  # <- renommer ici pour ton template
    }
