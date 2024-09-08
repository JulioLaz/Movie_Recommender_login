import streamlit as st
import pandas as pd
import ddbb
import similitud_knn as sim_knn
import ver_poster
import ver_poster_user_new as vpun
import text_desplazado as tdz


@st.cache_data(ttl=300)
def df_final():
    # df_ratings=load_df_ratings()
    df_ratings=ddbb.df_concat()
    df_movies = ddbb.load_df_movies()
    df_final = pd.merge(df_ratings, df_movies, on='movieId')
    df_final.dropna(inplace=True)
    return df_final

def load_just_for_you_data():
    df_final = ddbb.df_final()
    df_poster = ddbb.load_df_poster()
    return df_final, df_poster

def just_for_you_section():
    userId = st.session_state.get("user_id")
    df_ratings = ddbb.df_concat()
    if userId in df_ratings['userId'].values:    
        st.session_state.reload_data = True  # Forzar recarga de datos
        
        if st.session_state.reload_data:
            df_final, df_poster = load_just_for_you_data()
            st.session_state.df_final = df_final
            st.session_state.df_poster = df_poster
            st.session_state.reload_data = False
        else:
            df_final = st.session_state.df_final
            df_poster = st.session_state.df_poster

        tdz.title_poster_just('3rem','Movie recommendations just for you!')

        recommended_movies, movies_seen = sim_knn.recomendacion_knn(userId)
        df_final = df_final[df_final['movieId'].isin(movies_seen)]
        df_final = df_final.groupby(['movieId','title']).mean('rating').reset_index()
        df_poster_final = pd.merge(df_final, df_poster, on='movieId', how='left')

        if 'poster_path_full' in recommended_movies.columns:
            num_movies = 10  # Asumiendo que quieres mostrar 10 películas, ajusta según sea necesario
            lista_poster = list(recommended_movies['poster_path_full'].head(num_movies))
            lista_originalTitle = list(recommended_movies['title'].head(num_movies))
            lista_tconst = list(recommended_movies['imdb_id'].head(num_movies))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(num_movies))
            lista_years = list(recommended_movies['year'].head(num_movies))
            ver_poster.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating, lista_years)

        st.write(f"""<h1 style="color: gold; font-size: 2rem; height: 3rem; text-align: center; padding: 0px;margin:20px">
                Here are the movies you've already rated!
                </h1>""", unsafe_allow_html=True)
        
        lista_poster = list(df_poster_final['poster_path_full'])
        lista_originalTitle = list(df_poster_final['title'])
        lista_tconst = list(df_poster_final['imdb_id'])
        lista_averageRating = list(round(df_poster_final['rating'], 2))
        lista_years = list(df_poster_final['year'])
        vpun.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating, lista_years)
        pass
    else:
        tdz.title_poster_just('5rem', 'Rate movies with stars so it can recommend the best stuff for you!')
        pass    