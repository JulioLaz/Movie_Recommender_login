import pandas as pd
import zipfile
import requests
import streamlit as st
from io import BytesIO
import ddbb_postgreSQL as dbsql

url_login_api='https://jbkdzgglmrhzbzrjomwn.supabase.co'

path_img = 'https://i0.wp.com/image.tmdb.org/t/p/w300'
url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
response = requests.get(url)
zip_file = BytesIO(response.content) 

@st.cache_data(ttl=300)
def load_df_movies():
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        with zip_ref.open('ml-latest-small/movies.csv') as file:
            df_movies = pd.read_csv(file)
            # df_movies = pd.read_csv('data/ml-latest-small/movies.csv')
            df_movies = df_movies.dropna()
            df_movies = df_movies.drop_duplicates(subset=['movieId'])
            # df_movies['genres'] = df_movies['genres'].str.replace('|', ' ')
            df_movies['genre_set'] = df_movies['genres'].apply(lambda x: set(x.split('|')))
            df_movies['genres'] = df_movies['genres'].str.replace('|', ' ', regex=False)

            df_movies['movieId'] = df_movies['movieId'].astype('uint32')
            df_movies['title'] = df_movies['title'].astype(object)
            df_movies['genres'] = df_movies['genres'].astype(object)
        #  df_movies['content'] = df_movies['content'].astype(object)
            # df_movies['genre_set'] = df_movies['genre_set'].astype(object)
            df_movies['year'] = df_movies['title'].str.extract(r'\((\d{4})\)') # Extraer el año de la columna title y crear la nueva columna year
            df_movies['year'] = df_movies['year'].fillna(0).astype('uint16')
            df_movies['title'] = df_movies['title'].str.replace(r'\s*\(\d{4}\)$', '', regex=True) # Dejar sólo el title, eliminando el año:
    return df_movies

@st.cache_data(ttl=300)
def load_df_ratings():
 with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    with zip_ref.open('ml-latest-small/ratings.csv') as file:
        df_ratings = pd.read_csv(file)
        df_ratings = df_ratings.dropna()
        df_ratings = df_ratings.drop_duplicates(subset=['movieId', 'userId'])
        df_ratings['movieId'] = df_ratings['movieId'].astype('uint32')
        df_ratings['userId'] = df_ratings['userId'].astype('uint32')
        df_ratings['rating'] = df_ratings['rating'].astype(float)
        df_ratings['timestamp'] = pd.to_datetime(df_ratings['timestamp'], unit='s')
    return df_ratings

@st.cache_data(ttl=300)
def load_df_links():
 with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    with zip_ref.open('ml-latest-small/links.csv') as file:
        df = pd.read_csv(file)
        df = df.dropna()
        df = df.drop_duplicates(subset=['movieId'])
        df['movieId'] = df['movieId'].astype('uint32')
        df['imdbId'] = df['imdbId'].astype('uint32')
        df['imdbId'] = df['imdbId'].apply(lambda x: f"tt{x:07d}")
    return df[['movieId','imdbId']]
# print("load_df_links():",load_df_links().head())

@st.cache_data(ttl=300)
def load_df_poster():
   file_id = '1--35QAVDqzC9Z_K3eigB97aGy3FD_K3e'
   url = f'https://drive.google.com/uc?export=download&id={file_id}'
   df_poster = pd.read_csv(url)
   # df_poster=pd.read_csv('/content/drive/MyDrive/Bootcamp-Alejo-projects/movie_recommender/df_merged_poster_links.csv')
   df_poster = df_poster.dropna()
   df_poster = df_poster.drop_duplicates(subset=['movieId'])
   df_poster['poster_path_full'] = df_poster['poster_path'].apply(lambda x: f"{path_img}{x}")
   df_poster.drop('poster_path', axis=1, inplace=True)
   return df_poster

@st.cache_data(ttl=300)
def df_merge_movies_ratings():
    df_ratings=load_df_ratings()
    df_movies = load_df_movies()
    df_poster = load_df_poster()
    df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
    df = pd.merge(df_movies, df_average_ratings, on='movieId', how='left')
    df = pd.merge(df, df_poster, on='movieId', how='left')
    df = df.explode('genres')
    return df

@st.cache_data(ttl=300)
def df_final_original():
    # df_ratings=load_df_ratings()
    df_ratings=load_df_ratings()
    df_movies = load_df_movies()
    df_final = pd.merge(df_ratings, df_movies, on='movieId')
    df_final.dropna(inplace=True)
    return df_final

@st.cache_data(ttl=300)
def df_final():
    # df_ratings=load_df_ratings()
    df_ratings=df_concat()
    df_movies = load_df_movies()
    df_final = pd.merge(df_ratings, df_movies, on='movieId')
    df_final.dropna(inplace=True)
    return df_final

@st.cache_data(ttl=300)
def df_last_years():
    df_links=load_df_links()
    df_movies = load_df_movies()[['movieId','title','genres','year']]
    df = pd.merge(df_links, df_movies, on='movieId')
    df.dropna(inplace=True)
    df=df.nlargest(20,'year')
    return df
# print("df_final():",df_final().head())

@st.cache_data(ttl=300)
def new_user_rate():
    new_user=dbsql.extraer_datos()
    return new_user

@st.cache_data(ttl=300)
def df_concat():
    df_new_ratings=new_user_rate()[['userId','movieId','rating']]
    # df_new_ratings=dbsql.extraer_datos()[['userId','movieId','rating']]
    df_ratings=load_df_ratings()[['userId','movieId','rating']]
    df = pd.concat([df_ratings, df_new_ratings])
    df = df.groupby(['userId','movieId']).mean('rating').reset_index()
    return df


# print('df_final: ', df_poster_final.columns)
# print(new_user_rate().columns)
