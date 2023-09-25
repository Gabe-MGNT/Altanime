from django.contrib import admin

# Register your models here.

from search_anime.models import Anime

# listings/admin.py

from django.contrib import admin


class AdminAnime(admin.ModelAdmin):  # nous insérons ces deux lignes..
    list_display = ('id', 'title') # liste les champs que nous voulons sur l'affichage de la liste

admin.site.register(Anime, AdminAnime)