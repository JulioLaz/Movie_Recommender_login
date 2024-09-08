import ddbb
import pandas as pd

def recomendacion_populares():
    df_final = ddbb.df_final()
    df_poster = ddbb.load_df_poster() 
    vote_counts = df_final['title'].value_counts()
    df_popular_movies = df_final[df_final['title'].isin(vote_counts[vote_counts > 210].index)]
    df_movie_stats = df_popular_movies.groupby(['title','movieId','year']).agg(
        mean_rating=('rating', 'mean'),
        vote_count=('title', 'count')
    ).reset_index()

    m = df_movie_stats['vote_count'].quantile(.9)  # Calculate the minimum number of votes required (m)
    C = df_final['rating'].mean()  # Calculate the average rating of all movies (C)
    df_movie_stats['bayesian_average'] = (df_movie_stats['vote_count'] / (df_movie_stats['vote_count'] + m)) * df_movie_stats['mean_rating'] + (m / (df_movie_stats['vote_count'] + m)) * C
    df_movie_stats = df_movie_stats.nlargest(10, 'bayesian_average')
    df_poster_pop = pd.merge(df_movie_stats, df_poster, on='movieId', how='left')
    
    return df_poster_pop

print('df_poster_pop: ', recomendacion_populares().columns)
