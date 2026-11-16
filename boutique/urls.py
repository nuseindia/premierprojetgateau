from django.urls import path

from . import views

urlpatterns = [
        
    path('', views.boutique, name="boutique"),
    path('chariot/', views.chariot, name="chariot"),
    path('caisse/', views.caisse, name="caisse"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_commande/', views.processCommande, name="process_commande"),  
    path('accueil/', views.accueil, name="accueil"),  
]
