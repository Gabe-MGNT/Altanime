from django.db import models
from search_anime.models import Anime
# Create your models here.


class SimilarityMatrix(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    matrice = models.JSONField()  