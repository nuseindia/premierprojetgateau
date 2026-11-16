import json
from . models import *

def cookieChariot(request):
    try:
        chariot = json.loads(request.COOKIES['chariot'])
    except:
        chariot = {}

    print('Chariot:', chariot)
    items = []
    commande = {'get_chariot_total':0, 'get_chariot_items':0, 'shipping':False}
    chariotItems = commande['get_chariot_items']

    for i in chariot:
        try:
            chariotItems += chariot[i]["quantite"]

            produit = Produit.objects.get(id=i)
            total = (produit.prix * chariot[i]["quantite"])

            commande['get_chariot_total'] += total
            commande['get_chariot_items'] += chariot[i]["quantite"]

            item = {
                'produit':{
                    'id':produit.id,
                    'nom':produit.nom,
                    'prix':produit.prix,
                    'imageURL':produit.imageURL,
                },
                    'quantite':chariot[i]["quantite"],
                    'get_total':total,                    
            }
            items.append(item)

            if produit.digital == False:
                commande['shipping'] = True
        except:
            pass
    return {'chariotItems':chariotItems, 'commande':commande, 'items': items}

def guestCommande(request, data):
    print('User non authentifié...')
    print('COOKIES:', request.COOKIES)
    nom = data['form']['nom']
    email = data['form']['email']

    cookieData = cookieChariot(request)
    items = cookieData['items']

    client, created = Client.objects.get_or_create(
        email=email,
        )
    client.nom = nom
    client.save()

    commande = Commande.objects.create(
        client=client,
        etat=False,
        )
    for item in items:
        produit = Produit.objects.get(id=item['produit']['id'])

        articleCom = ArticleCom.objects.create(
                produit=produit,
                commande=commande,
                quantite=item['quantite']
                )
    return client, commande

def chariotData(request):
    if request.user.is_authenticated:
       client = request.user.client
       commande, created = Commande.objects.get_or_create(client=client, etat=False)
       items = commande.articlecom_set.all()
       chariotItems = commande.get_chariot_items
    else:
        cookieData = cookieChariot(request)
        chariotItems = cookieData['chariotItems']
        commande = cookieData['commande']
        items = cookieData['items']
    return{'chariotItems':chariotItems, 'commande':commande, 'items': items}
