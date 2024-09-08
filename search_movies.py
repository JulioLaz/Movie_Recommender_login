import streamlit as st
import ddbb
import title_poster_genre as tpg
import pandas as pd
import view_posters

def search_movies():
    df_final=ddbb.df_final()
    df_poster=ddbb.load_df_poster()

    col1, col2 = st.columns(2)
    with col1:
        tpg.title_poster_genre('','Find the movie you like best!')
    with col2:
        df_final=df_final.drop_duplicates('movieId')
        movie_titles = df_final['title'].tolist()
        title='Matrix, The'
        default_index = movie_titles.index(title) if title in movie_titles else 0
        selected_title = st.selectbox("", movie_titles, index=default_index, label_visibility="collapsed")

    df_final = df_final.groupby(['movieId','title']).mean('rating').reset_index()
    df_poster_final = pd.merge(df_final, df_poster, on='movieId', how='left')
    df_poster_final = df_poster_final[df_poster_final['title'] == selected_title]
    lista_tconst = list(df_poster_final['imdb_id'])
    lista_averageRating = list(round(df_poster_final['rating'], 2))

    view_posters.view_movie_details_new_user(lista_tconst[0],lista_averageRating[0])