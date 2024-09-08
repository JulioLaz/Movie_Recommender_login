import ddbb
import pandas as pd

def similitud_jaccard(set1, set2):
    """Calcula la similitud de Jaccard entre dos conjuntos."""
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def recomendacion_jaccard(movie_id):
    n_recommendations=10
    df=ddbb.load_df_movies()
    df_ratings=ddbb.load_df_ratings()
    df_poster=ddbb.load_df_poster()
    input_features = df[df['movieId'] == movie_id]['genre_set'].values[0]
    df['similarity'] = df['genre_set'].apply(lambda x: similitud_jaccard(input_features, x))
    df.sort_values('similarity', ascending=False, inplace=True)
    df=df.nlargest(n_recommendations,'similarity')
    df.sort_values('year', ascending=False, inplace=True)
    df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
    df_poster_jaccard = pd.merge(df, df_average_ratings, on='movieId', how='left')
    df_poster_jaccard = pd.merge(df_poster_jaccard, df_poster, on='movieId', how='left')
    df_poster_jaccard = df_poster_jaccard[df_poster_jaccard['movieId'] != movie_id]
    return df_poster_jaccard

# print('recomendacion_jaccard: ', recomendacion_jaccard(58559).columns)