from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from search_anime.models import Anime
from rest_framework.decorators import action

from search_anime.serializers import AnimeSerializer, AnimeDetailSerializer
import random
# Create your views here.
def Index(request):
    return render(request, "index_hol.html")

def Game(request):
     return render(request, "game_templatev2.html")


class GetNewAnime(ReadOnlyModelViewSet):
    serializer_class = AnimeDetailSerializer

    def get_queryset(self):

            rank_number = int(self.request.query_params.get("rank", None))
            range_start = float(self.request.query_params.get("range_start", None))
            range_end = float(self.request.query_params.get("range_end", None))
            
            anime_in_range = Anime.objects.filter(popularity__range=[rank_number*range_start, rank_number*range_end])
            items = list(anime_in_range)
            random_items = random.sample(items, 1)

            return random_items




