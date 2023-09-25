from rest_framework.serializers import ModelSerializer
from search_anime.models import Anime

class AnimeSerializer(ModelSerializer):

    class Meta:
        model = Anime
        fields = ["id", "title", "summary", "aired_date", "image"]


class AnimeDetailSerializer(ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'