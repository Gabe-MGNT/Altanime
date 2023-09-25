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
from recommandations.models import SimilarityMatrix
import random
import numpy as np
import pandas as pd
import time
import operator


# Create your views here.

from search_anime.models import Anime
from search_anime.serializers import AnimeSerializer, AnimeDetailSerializer

def SearchView(request):
    return render(request, "search.html")

def BaseView(request):
    return render(request, "recommander.html")


class GetRecommandations(ReadOnlyModelViewSet):

    serializer_class = AnimeSerializer



    def get_queryset(self):
        title_query = self.request.query_params.get("title", None)
        id_anime = int(self.request.query_params.get("id", 1))

        weight_themes = int(self.request.query_params.get("weight_themes", None))
        weight_studio = int(self.request.query_params.get("weight_studio", None))
        weight_summary = int(self.request.query_params.get("weight_summary", None))
        weight_genres = int(self.request.query_params.get("weight_genres", None))


        start = time.time()
        similarities_data = SimilarityMatrix.objects.filter(anime_id=id_anime)[0]
        sim_matrix = similarities_data.matrice

        sim_themes = sim_matrix["themes_sim"]
        sim_studios = sim_matrix["studio_sim"]
        sim_summary = sim_matrix["summary_sim"]
        sim_genres = sim_matrix["genre_sim"]
        # Get the pairwsie similarity scores of all movies with that movie


        sim_themes_score = [x[1] for x in sim_themes]
        sim_studios_score = [x[1] for x in sim_studios]
        sim_summary_score = [x[1] for x in sim_summary]
        sim_genre_score = [x[1] for x in sim_genres]

        anime_sim_index = [x[0] for x in sim_genres]



        #cosine_global_sim = (weights[0] * self.sim_genres) + (weights[1] * self.sim_studios) + (weights[2] * self.sim_summary) + (weights[3] * self.sim_genres)
        #similarities = [self.sim_themes[idx], self.sim_studios[idx], self.sim_summary[idx], self.sim_genres[idx]]
        #similarities = [np.array(sim_themes), np.array(sim_studios), np.array(sim_summary), np.array(sim_genres)]
        similarities = [np.array(sim_themes_score), np.array(sim_studios_score), np.array(sim_summary_score), np.array(sim_genre_score)]

        weights = np.array([weight_themes,weight_studio,weight_summary,weight_genres])

        cosine_global_sim = sum(weight * similarity for weight, similarity in zip(weights, similarities))

        zipped_array = zip(anime_sim_index, cosine_global_sim)
        sorted_zipped_array = sorted(zipped_array, key=lambda x: x[1], reverse=True)
        top_10_elements = sorted_zipped_array[:10]


        recommandations = [x[0] for x in top_10_elements]

        """
        #sim_scores = list(enumerate(cosine_global_sim[idx]))
        sim_scores = list(enumerate(cosine_global_sim))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        top_similar = sim_scores[1:10+1]

        movie_indices = [i[0] for i in top_similar]
        print(sim_matrix["indices"])
        recommandations = pd.Series(sim_matrix["indices"])[movie_indices].index
        """

        

         
        print("TIME TO RECOMMAND : ", time.time()-start)

        """query = Q()
        for titre in recommandations:
            print(titre)
            query |= Q(id__icontains=titre)  # Vous pouvez ajuster le type de recherche ici

        recommanded_animes = Anime.objects.filter(query)
"""
        recommanded_animes = Anime.objects.filter(id__in=recommandations)
        print(recommanded_animes)
        return  recommanded_animes
