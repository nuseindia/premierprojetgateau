from django.contrib import admin

from .models import *

admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Commande)
admin.site.register(ArticleCom)
admin.site.register(AdresseLiv)
