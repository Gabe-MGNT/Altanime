from search_anime.models import Anime
from recommandations.models import SimilarityMatrix
import csv
import os
from recommandations.src.similarities_matrix import *


df = pd.read_csv("./anime.csv")
df = df.fillna('')

genre_sim = get_genres_similarities()




studios_sim = get_studios_similarities()
themes_sim = get_themes_similarities()
summary_sim = get_summary_similarities()

genre_sim_list = list(genre_sim)
themes_sim_list = list(themes_sim)
studio_sim_list = list(studios_sim)



SimilarityMatrix.objects.all().delete()

rank= -1
for id, sim_matrix in summary_sim:

    print(id)

    rank += 1

    try:
        int_id = int(id)
    except ValueError:
        continue
    
    anime_w_id = Anime.objects.get(id=int_id)


    genre_sim_id = genre_sim_list[rank]
    themes_sim_id = themes_sim_list[rank]
    studio_sim_id = studio_sim_list[rank]

    matrice_similarite = {
        "summary_sim": list(sim_matrix),
        "studio_sim" : list(studio_sim_id[1]),
        "themes_sim": list(themes_sim_id[1]),
        "genre_sim" : list(genre_sim_id[1]),
        } 

    nouvelle_similarite = SimilarityMatrix(anime=anime_w_id, matrice=matrice_similarite)
    nouvelle_similarite.save()

