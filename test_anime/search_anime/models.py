from django.db import models

# Create your models here.


class Anime(models.Model):

    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=150000)
    aired_date = models.CharField(max_length=200)
    episodes = models.CharField(max_length=100)
    favorites = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    studios = models.CharField(max_length=500)
    themes =models.CharField(max_length=500)
    type = models.CharField(max_length=500)
    id = models.IntegerField(primary_key=True)
    popularity = models.IntegerField()
    ranking = models.CharField(max_length=100)
    image = models.ImageField(upload_to='anime_images/', null=True, blank=True)

    def __str__(self):
        return self.title