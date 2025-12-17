from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),

    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('tablebord/', views.tablebord, name="tablebord"),
    path('contact/', views.contact, name="contact"),
    path('rapport/', views.rapport_view, name="rapport"),
    path('parametre/', views.parametre_view, name='parametre'),

    path('notifications/', include('notifications.urls')),
    path('notification/lire/<int:notif_id>/', views.lire_notification, name='lire_notification'),
    path('notifications/read/<int:notif_id>/', views.mark_as_read, name='mark_as_read'),
    
    path('logout/', views.deconnexion, name='logout'),
    path('quitter/', views.quitter, name='quitter'),
    
  
    path('modeles/', views.liste_modeles, name='liste_modeles'),
    path('modeles/ajouter/', views.ajouter_modele, name='ajouter_modele'),
    path('modeles/modifier/<int:id>/', views.modifier_modele, name='modifier_modele'),
    path('modeles/supprimer/<int:id>/', views.supprimer_modele, name='supprimer_modele'),


    path('salon/', views.liste_salons, name="liste_salons"),
    path('salon/ajouter/', views.ajouter_salon, name="ajouter_salon"),
    path('salon/modifier/<uuid:id>/', views.modifier_salon, name="modifier_salon"),
    path('salon/supprimer/<uuid:id>/', views.supprimer_salon, name="supprimer_salon"),
    path('salon/detail/<uuid:id>/', views.detail_salon, name="detail_salon"),

    path('client/', views.liste_clients, name="liste_clients"),
    path('clients/ajouter_client/', views.ajouter_client, name="ajouter_client"),
    path('clients/modifier_client/<int:id>/', views.modifier_client, name="modifier_client"),
    path('clients/supprimer_client/<int:id>/', views.supprimer_client, name="supprimer_client"),

    path('produits/', views.liste_produits, name="liste_produits"),
    path('produits/ajouter/', views.ajouter_produit, name="ajouter_produit"),
    path('produits/modifier/<int:id>/', views.modifier_produit, name="modifier_produit"),
    path('produits/supprimer/<int:id>/', views.supprimer_produit, name="supprimer_produit"),
    
    path('employes/', views.liste_employes, name="liste_employes"),
    path('employes/ajouter/', views.ajouter_employe, name="ajouter_employe"),
    path('employes/modifier/<int:id>/', views.modifier_employe, name="modifier_employe"),
    path('employes/supprimer/<int:id>/', views.supprimer_employe, name="supprimer_employe"),

    path('services/', views.liste_services, name="liste_services"),
    path('services/ajouter/', views.ajouter_service, name="ajouter_service"),
    path('services/modifier/<int:id>/', views.modifier_service, name="modifier_service"),
    path('services/supprimer/<int:id>/', views.supprimer_service, name="supprimer_service"),

    path('prestation/', views.liste_prestations, name="liste_prestations"),
    path('prestation/ajouter/', views.ajouter_prestation, name="ajouter_prestation"),
    path('prestation/modifier/<int:id>/', views.modifier_prestation, name="modifier_prestation"),
    path('prestation/supprimer/<int:id>/', views.supprimer_prestation, name="supprimer_prestation"),
    
    path('rdv/', views.liste_rdv, name="liste_rdv"),
    path('rdv/ajouter/', views.ajouter_rdv, name="ajouter_rdv"),
    path('rdv/supprimer/<int:id>/', views.supprimer_rdv, name="supprimer_rdv"),
    path('rdv/modifier/<int:id>/', views.modifier_rdv, name='modifier_rdv'),

    path('paiement/', views.liste_paiements, name="liste_paiements"),
    path('paiement/ajouter/', views.ajouter_paiement, name="ajouter_paiement"),
    path('paiement/modifier/<int:id>/', views.modifier_paiement, name="modifier_paiement"),
    path('paiement/supprimer/<int:id>/', views.supprimer_paiement, name="supprimer_paiement"),
    path('facture/<int:paiement_id>/', views.facture_pdf, name='facture_pdf'),
    path('paiement/<int:paiement_id>/', views.detail_paiement, name='detail_paiement'),
    path('paiements/', views.historique_paiements, name='historique_paiements'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
