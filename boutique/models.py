from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nom = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prix = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.CharField(max_length=1000, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.nom

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Commande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    datecom = models.DateTimeField(auto_now_add=True)
    etat = models.BooleanField(default=False, null=True, blank=False)
    transactionid = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_chariot_total(self):
        commandeitems = self.articlecom_set.all()
        total = sum([item.get_total for item in commandeitems]) 
        return total

    @property
    def get_chariot_items(self):
        commandeitems = self.articlecom_set.all()
        total = sum([item.quantite for item in commandeitems]) 
        return total

    @property
    def shipping(self):
        shipping = False
        article_coms = self.articlecom_set.all()
        for i in article_coms:
            if i.produit.digital == False:
                shipping = True
        return shipping



class ArticleCom(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True)
    quantite = models.IntegerField(default=0, null=True, blank=True)
    dateart = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.produit.prix * self.quantite
        return total


class AdresseLiv(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    commande = models.ForeignKey(Commande, on_delete=models.SET_NULL, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True)
    ville = models.CharField(max_length=200, null=True)
    coderecu = models.CharField(max_length=200, null=True)
    codepostal = models.CharField(max_length=200, null=True)
    dateliv = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.adresse 
