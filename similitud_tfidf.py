from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import ddbb
import pandas as pd

def recomendacion_tf_idf(movie_id):
   n_recommendations=10
   df_movies=ddbb.load_df_movies()
   df_ratings=ddbb.load_df_ratings()
   df_poster=ddbb.load_df_poster()

   vectorizer = TfidfVectorizer(stop_words='english')
   feature_vectors = vectorizer.fit_transform(df_movies['genres'])
   cosine_sim = cosine_similarity(feature_vectors,feature_vectors)

   idx = df_movies[df_movies['movieId'] == movie_id].index[0]
   sim_scores = list(enumerate(cosine_sim[idx]))
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   sim_scores = [x for x in sim_scores if x[0] != idx]
   movie_indices = [x[0] for x in sim_scores[:n_recommendations]]
   recommended_movies = df_movies.iloc[movie_indices]
   recommended_movies = recommended_movies.copy()
   recommended_movies['distance'] = [x[1] for x in sim_scores[:n_recommendations]]
   df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
   df_poster_tfidfvec = pd.merge(recommended_movies, df_average_ratings, on='movieId', how='left')
   df_poster_tfidfvec.drop(['genres','genre_set'], axis=1,inplace=True)
   df_poster_tfidfvec = pd.merge(df_poster_tfidfvec, df_poster, on='movieId', how='left')
   df_poster_tfidfvec = df_poster_tfidfvec[df_poster_tfidfvec['movieId'] != movie_id]

   return df_poster_tfidfvec

print('recomendacion_tf_idf(movie_id): ',recomendacion_tf_idf(1).columns)