import cachetools
import pickle
import numpy as np
import time
import pandas as pd
from recommandations.src import similarities_matrix
from django.core.cache import cache

class Recommande:

    def __init__(self, cache_file:str="cache.pkl"):
        self.cache_file = cache_file
        self.cache = None
        self.cache_read = None
        self.complete = True

        self.indices = None
        self.sim_genres = None
        self.sim_studios = None
        self.sim_summary = None
        self.sim_themes = None
  
        start = time.time()
        self.check_cache()
        print("TME CHECK CACHE : ", time.time()-start)






    def check_cache(self):

        start = time.time()
        if  cache.get("indices") is None:
            indices = similarities_matrix.get_indices()
            self.indices = indices
            cache.set("indices", indices, timeout=None)
        else:
            self.indices = cache.get("indices")
        print("TIME GET INDICES : ", time.time()-start)

        """
        if self.need_update()==False:
            return
        """
        return

        anime_data_dict = {}
        for index, anime_title in enumerate(self.indices.index):
            if  cache.get(anime_title) is not None:
                continue

            if self.sim_studios is None:
                self.sim_genres = similarities_matrix.get_genres_similarities()
                self.sim_studios = similarities_matrix.get_studios_similarities()
                self.sim_summary = similarities_matrix.get_summary_similarities()
                self.sim_theme = similarities_matrix.get_themes_similarities()

            anime_data = {
            "sim_genre": self.sim_genres[index],
            "sim_studios": self.sim_studios[index],
            "sim_summary": self.sim_summary[index],
            "sim_theme": self.sim_theme[index]
            }
            anime_data_dict[anime_title] = anime_data
            #cache.set(anime_title, anime_data, timeout=None)
        cache.set_many(anime_data_dict, timeout=None)


    def need_update(self):
        start = time.time()
        random_samples = self.indices.sample(n=50).index
        none_counter = 0

        for sample in random_samples:
            if cache.get(sample) is None:
                none_counter += 1

            if none_counter > 100:
                return True
        print("CHECK INTEGRITY : ", time.time()-start)
        return False






    def get_recommendations(self, title, weights, num_recommend = 10):
        similarities_data = cache.get(title)
        sim_themes = similarities_data.get("sim_theme")
        sim_studios = similarities_data.get("sim_studios")
        sim_summary = similarities_data.get("sim_summary")
        sim_genres = similarities_data.get("sim_genre")
        # Get the pairwsie similarity scores of all movies with that movie

        #cosine_global_sim = (weights[0] * self.sim_genres) + (weights[1] * self.sim_studios) + (weights[2] * self.sim_summary) + (weights[3] * self.sim_genres)
        #similarities = [self.sim_themes[idx], self.sim_studios[idx], self.sim_summary[idx], self.sim_genres[idx]]
        similarities = [sim_themes, sim_studios, sim_summary, sim_genres]

        cosine_global_sim = sum(weight * similarity for weight, similarity in zip(weights, similarities))

        #sim_scores = list(enumerate(cosine_global_sim[idx]))
        sim_scores = list(enumerate(cosine_global_sim))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        top_similar = sim_scores[1:num_recommend+1]

        movie_indices = [i[0] for i in top_similar]

        return self.indices[movie_indices].index

