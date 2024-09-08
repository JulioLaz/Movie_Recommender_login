import streamlit as st
import ddbb
import title_poster_genre as tpg
import line_gold
import similitud_tfidf as sim_tfidf
import ver_poster
num_movies=8

def top_rated():
    df_final=ddbb.df_final()
    df_final = df_final.drop_duplicates(subset='title', keep='first')
    col1, col2 = st.columns(2)
    with col1:
        tpg.title_poster_genre('','People who watched this movie also loved these!')

        # st.subheader("People who watched this movie also loved these!")
    with col2:
        movie_titles = df_final['title'].tolist()
        title='Titanic'
        default_index = movie_titles.index(title) if title in movie_titles else 0
        selected_title = st.selectbox("Select a movie you like: Connect with other movie enthusiasts and get personalized recommendations", movie_titles, index=default_index)
    
    line_gold.line_gold()

    if selected_title:
        movie_id = df_final[df_final['title'] == selected_title]['movieId'].values[0]
        recommended_movies = sim_tfidf.recomendacion_tf_idf(movie_id)

        if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(num_movies))
            lista_originalTitle = list(recommended_movies['title'].head(num_movies))
            lista_tconst = list(recommended_movies['imdb_id'].head(num_movies))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(num_movies))
            lista_years = list(recommended_movies['year'].head(num_movies))

            ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating,lista_years)   