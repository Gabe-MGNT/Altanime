from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.paginator import Paginator
from django.db.models import Q
import requests
import random

# Create your views here.

from search_anime.models import Anime
from search_anime.serializers import AnimeSerializer, AnimeDetailSerializer

def SearchView(request):
    return render(request, "search.html")

def BaseView(request):

    animes = Anime.objects.all()


    return render(request, "index.html", {"animes":animes})

from django.http import JsonResponse

def AnimeDetail(request, id):
    if request.method == "GET":
        anime = requests.get("http://127.0.0.1:8000/api/list/"+str(id), params=request.GET).json()

    print("anime : ", anime)

    return render(request, "anime_card_template.html", {"anime":anime})


class AnimeView(ReadOnlyModelViewSet):

    class CustomPageNumberPagination(PageNumberPagination):
        page_size = 10
        page_size_query_param = 'page_size'
        max_page_size = 30

    serializer_class = AnimeSerializer
    detail_serializer_class = AnimeDetailSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):

        return Anime.objects.filter()
    def get_serializer_class(self):

        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    def filter_queryset(self, queryset):
        search_query = self.request.query_params.get("search", None)

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query)| Q(summary__icontains=search_query))
        return queryset


class RandomAnime(ReadOnlyModelViewSet):

    serializer_class = AnimeDetailSerializer

    def get_queryset(self):

        samples = self.request.query_params.get("samples")

        if samples==None or samples.isnumeric() is False:
            samples = 1
        else:
            samples = int(samples)

        items = list(Anime.objects.all())
        random_items = random.sample(items, samples)
        return random_items