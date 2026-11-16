from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieChariot, chariotData, guestCommande


def boutique(request):
    
     data = chariotData(request)
     chariotItems = data['chariotItems']

     produits = Produit.objects.all()
     context = {'produits':produits, 'chariotItems':chariotItems}
     return render(request, 'boutique/boutique.html', context)

def chariot(request):

     data = chariotData(request)
     chariotItems = data['chariotItems']
     commande = data['commande']
     items = data['items']          
          
     context = {'items':items, 'commande':commande, 'chariotItems':chariotItems}
     return render(request, 'boutique/chariot.html', context)

def caisse(request):
     
     data = chariotData(request)
     chariotItems = data['chariotItems']
     commande = data['commande']
     items = data['items']

     context = {'items':items, 'commande':commande, 'chariotItems':chariotItems}
     return render(request, 'boutique/caisse.html', context)



def updateItem(request):
     return JsonResponse('Article ajouté', safe=False)

def updateItem(request):
     data = json.loads(request.body)
     produitId = data['produitId']
     action = data['action']

     print('Action:', action)
     print('produitId:', produitId)

     client = request.user.client
     produit = Produit.objects.get(id=produitId)
     commande, created = Commande.objects.get_or_create(client=client, etat=False)

     articlecom, created = ArticleCom.objects.get_or_create(commande=commande, produit=produit)

     if action == 'add':
          articlecom.quantite = (articlecom.quantite + 1)
     elif action == 'remove':
          articlecom.quantite = (articlecom.quantite - 1)
     
     articlecom.save()

     if articlecom.quantite <= 0:
          articlecom.delete()

     return JsonResponse('article est ajouté', safe=False)

def processCommande(request):
     print('Data:', request.body)
     return JsonResponse('Payement complet!', safe=False)

def processCommande(request):
     comid = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     
     if request.user.is_authenticated:
          client = request.user.client
          commande, created = Commande.objects.get_or_create(client=client, etat=False)
          total = float(data['form']['total'])
          commande.comid = comid

          if total == commande.get_chariot_total:
               commande.etat = True
          commande.save()

          if commande.shipping == True:
               AdresseLiv.objects.create(
                    client=client,
                    commande=commande,
                    adresse=data['shipping']['adresse'],
                    ville=data['shipping']['ville'],
                    coderecu=data['shipping']['coderecu'],
                    codepostal=data['shipping']['codepostal'],
               )

     else:
          print('Utilisateur non connecté ...')
     return JsonResponse('Payment complet!', safe=False)

def accueil(request):
     data = chariotData(request)
     chariotItems = data['chariotItems']
     commande = data['commande']
     items = data['items']          
          
     context = {'items':items, 'commande':commande, 'chariotItems':chariotItems}
     return render(request, 'boutique/accueil.html', context)

     
