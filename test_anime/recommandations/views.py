from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.paginator import Paginator
from django.db.models import Q
import requests
from recommandations.src.find_recommandations import Recommande
import random
import numpy as np
import time

# Create your views here.

from search_anime.models import Anime
from search_anime.serializers import AnimeSerializer, AnimeDetailSerializer

def SearchView(request):
    return render(request, "search.html")

def BaseView(request):
    return render(request, "recommander.html")


class GetRecommandations(ReadOnlyModelViewSet):

    serializer_class = AnimeSerializer

    class CustomPageNumberPagination(PageNumberPagination):
        page_size = 10

    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        title_query = self.request.query_params.get("title", None)

        weight_themes = int(self.request.query_params.get("weight_themes", None))
        weight_studio = int(self.request.query_params.get("weight_studio", None))
        weight_summary = int(self.request.query_params.get("weight_summary", None))
        weight_genres = int(self.request.query_params.get("weight_genres", None))


        start = time.time()
        recommandations = Recommande("cache.pkl").get_recommendations(
            title=title_query,
            weights=np.array([weight_themes,weight_studio,weight_summary,weight_genres]),
            num_recommend=10
        )
        print("TIME TO RECOMMAND : ", time.time()-start)

        query = Q()
        for titre in recommandations:
            query |= Q(title__icontains=titre)  # Vous pouvez ajuster le type de recherche ici

        recommanded_animes = Anime.objects.filter(query)

        return  recommanded_animes
