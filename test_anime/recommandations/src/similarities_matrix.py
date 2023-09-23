import pandas as pd
import numpy as np
from recommandations.src.utils import get_cosine_similarity_from_column


df = pd.read_csv("./anime.csv")
df = df.fillna('')

def get_genres_similarities():
    return np.array(get_cosine_similarity_from_column(df, 'Genres', True))

def get_studios_similarities():
    return np.array(get_cosine_similarity_from_column(df, 'Studios', True))

def get_themes_similarities():
    return np.array(get_cosine_similarity_from_column(df, 'Themes', True))

def get_summary_similarities():
    return np.array(get_cosine_similarity_from_column(df, 'summary', False))

def get_indices():
    return pd.Series(df.index, index=df['title'])
