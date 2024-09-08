import pandas as pd
from sklearn.neighbors import NearestNeighbors
import ddbb
import numpy as np

def recomendacion_knn(user_input):
    df_final = ddbb.df_final()
    df_movies = ddbb.load_df_movies()
    df_ratings= ddbb.df_concat()
    df_poster=ddbb.load_df_poster()

    n_recommendations=10
    # if new_user <= user_input:
    if isinstance(user_input, int):
        print('Existing user')
        # print(df_ratings.userId.max())
        ratings_matrix = df_ratings.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(user_input)
        distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
    else:
        print('New user')
        new_user_ratings = pd.DataFrame({
            'userId': [df_ratings['userId'].max() + 1] * len(user_input),  # Match length to user_input
            # 'userId': [df_agg['userId'].max() + 1] * 2,
            'movieId': user_input.index,
            'rating': user_input.values})
        
        new_df_movies = new_user_ratings.merge(df_movies, on='movieId', how='left')
        selected_movie_genres = new_df_movies[new_df_movies['movieId'].isin(user_input.index)]['genre_set']
        selected_genres = set().union(*selected_movie_genres)
      #   print(selected_genres)
        df_final_filtered = df_final[df_final['genre_set'].apply(lambda x: bool(selected_genres & x))]
        # df_final_filtered=df_final_filtered.copy()
        df_final_filtered.drop_duplicates(subset=['movieId'], inplace=True)

        df_agg = df_final_filtered.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
        df_agg_final = pd.concat([df_agg, new_user_ratings], ignore_index=True)
        ratings_matrix = df_agg_final.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(df_agg_final.userId.max())

    max_neighbors = min(n_recommendations + 1, len(ratings_matrix_normalized))
    if max_neighbors >= 5:
        distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=max_neighbors)
    else:
        ratings_matrix = df_ratings.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(user_input)
        distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)

        # df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
        # df_agg_final = pd.concat([df_agg, new_user_ratings], ignore_index=True)
        # ratings_matrix = df_agg_final.pivot(index='userId', columns='movieId', values='rating')
        # avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        # ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        # knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        # knn_model.fit(ratings_matrix_normalized.values)
        # idx = ratings_matrix_normalized.index.get_loc(df_agg_final.userId.max())      
        # distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)

    distances = distances.flatten()[1:]
    indices = indices.flatten()[1:]

    similar_users = ratings_matrix_normalized.iloc[indices]
    # print('similar_users: ',similar_users.head(10))
    mean_ratings = similar_users.T.dot(distances) / np.sum(distances)
    df_mean_ratings = pd.DataFrame(mean_ratings, index=ratings_matrix_normalized.columns, columns=['mean_rating'])
    df_mean_ratings = df_mean_ratings.dropna()
    df_mean_ratings.sort_values('mean_rating', ascending=False, inplace=True)
    # print('df_mean_ratings: ',df_mean_ratings.head(10))
    # if isinstance(user_input, int):
    movies_seen = df_ratings[df_ratings['userId']==user_input]['movieId']
    # print('movies_seen: ', movies_seen[:10])
    # else:
        # movies_seen = df_agg_final[df_agg_final['userId'] == df_agg_final['userId'].max()]['movieId']
    df_mean_ratings = df_mean_ratings[~df_mean_ratings.index.isin(movies_seen)]
    df_mean_ratings = df_mean_ratings.sort_values('mean_rating', ascending=False)
    # print('df_mean_ratings: ', df_mean_ratings.head(10))
    recommended_movies = pd.merge(df_mean_ratings, df_final[['movieId', 'title', 'genres','year']], left_index=True, right_on='movieId')
    recommended_movies.drop_duplicates(subset=['movieId'], inplace=True)
    columnas=['movieId', 'title', 'genres','mean_rating','year']
    recommended_movies=recommended_movies[columnas].head(n_recommendations)

    df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
    df_poster_knn = pd.merge(recommended_movies, df_average_ratings, on='movieId', how='left')
    df_poster_knn_final = pd.merge(df_poster_knn, df_poster, on='movieId', how='left')
    df_poster_knn_final = df_poster_knn_final[~df_poster_knn_final['movieId'].isin(movies_seen)]
    return df_poster_knn_final,movies_seen

# print(recomendacion_knn(777))

df_final = ddbb.df_final_original()
df_movies = ddbb.load_df_movies()
df_ratings= ddbb.load_df_ratings()
# df_ratings= ddbb.df_concat()
df_poster=ddbb.load_df_poster()

df_final = df_final.drop_duplicates(subset=['userId', 'title'])
ratings_matrix = df_final.pivot(index='userId', columns='title', values='rating')
avg_ratings = ratings_matrix.mean(axis=1)
ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
knn_model = NearestNeighbors(metric='cosine', algorithm='auto')
# knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
knn_model.fit(ratings_matrix_normalized)

def recomendacion_knn_old_user(user_input):
    n_recommendations=10
    if isinstance(user_input, int):
        idx = ratings_matrix.index.get_loc(user_input)
        # idx = ratings_matrix_normalized.index.get_loc(user_input)
        distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
    # else:
    #     user_ratings = pd.Series(user_input).fillna(0).sub(avg_ratings.mean()).values.reshape(1, -1)
    #     distances, indices = knn_model.kneighbors(user_ratings, n_neighbors=n_recommendations + 1)
    distances, indices = distances.flatten()[1:], indices.flatten()[1:]
    similar_users_ratings = ratings_matrix_normalized.iloc[indices, :]
    weighted_ratings = similar_users_ratings.T.dot(1 - distances) / (1 - distances).sum()
    recommendations_df = pd.DataFrame(weighted_ratings, index=ratings_matrix.columns, columns=['weighted_score'])
    if isinstance(user_input, int):
        watched_movies = ratings_matrix.loc[user_input].dropna().index
        recommendations_df = recommendations_df[~recommendations_df.index.isin(watched_movies)]
    recommendations_df = recommendations_df.sort_values(by='weighted_score', ascending=False).head(n_recommendations)
    recommendations_df = recommendations_df.merge(df_movies[['title', 'genres','movieId','year']], left_index=True, right_on='title', how='left')
    df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
    df_poster_knn = pd.merge(recommendations_df, df_average_ratings, on='movieId', how='left')
    df_poster_knn_final = pd.merge(df_poster_knn, df_poster, on='movieId', how='left')
    movies_seen = df_ratings[df_ratings['userId']==user_input]['movieId']
    df_poster_knn_final = df_poster_knn_final[~df_poster_knn_final['movieId'].isin(movies_seen)]
    # print('recommendations_df:',recommendations_df)
    return df_poster_knn_final

# print('recomendacion_knn_old_user(50):', recomendacion_knn_old_user(50).columns)