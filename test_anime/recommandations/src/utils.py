import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer


def get_cosine_similarity_from_column(df, column_name, categorie=True):
    res = None
    if categorie == True:
        res =  encode_categories(df, column_name)
        return cosine_similarity(pd.DataFrame(list(res)))
    else:
        res =  encode_text(df, column_name)
        return cosine_similarity(res, res)


def encode_text(df, column_name):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df[column_name])
    return tfidf_matrix

def encode_categories(df, column_name):
    set_genres = get_unique_elements(df[column_name])
    set_genres.remove('')
    genres_list = list(set_genres)
    genres_array = np.array(genres_list).reshape(1,-1)

    le = MultiLabelBinarizer()
    le.fit(genres_array)

    def apply_le(x):
        if len(x)==0:
            return [0] * len(le.classes_)
        res = le.transform([x.split(",")])
        return res[0]
    
    return df[column_name].apply(apply_le)

def get_unique_elements(column):
    set_genre = set()
    for _, row in enumerate(column):
        try:
            genres = row.split(',')
            for genre in genres:
                set_genre.add(genre)
        except Exception:
            genre = row

            set_genre.add(genre)
    return set_genre