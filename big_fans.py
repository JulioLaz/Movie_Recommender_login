import streamlit as st
import ddbb
import title_poster_genre as tpg
import pandas as pd
import text_giro as tg
import similitud_knn as sim_knn
import ver_poster
from collections import Counter


num_movies=8
def big_fans():
    df_final=ddbb.df_final_original()
    movies = df_final.groupby('userId')['rating'].count().reset_index().sort_values(by='rating', ascending=False)
    user_rating_counts = dict(zip(movies.userId, movies.rating))
    user_options = [f"Usuario {userId} - voted movies: {count}" for userId, count in user_rating_counts.items()]
    col1,col2=st.columns(2)
    with col1:
        tg.giro('','Top picks for our biggest fans')

    with col2:
        col1,col2=st.columns(2)
        with col1:
               selected_user_option = st.selectbox('', user_options,label_visibility="collapsed")
               selected_user_id = int(selected_user_option.split()[1])    
            # user_genres_counts = dict(zip(df_genres.Genre, df_genres.Count))
            # user_options_genre = [f"{Genre} - Count: {Count}" for Genre, Count in user_genres_counts.items()]

        with col2:
            counter=movies[movies['userId']==selected_user_id]['rating'].values[0]
            st.write('Voted movies:',int(counter))
            user_movies = df_final[df_final['userId'] == selected_user_id]
            selected_movie_genres = user_movies['genre_set']
            all_genres = [genre for genre_set in selected_movie_genres for genre in genre_set]
            genre_counts = Counter(all_genres)
            df_genres = pd.DataFrame.from_dict(genre_counts, orient='index', columns=['Count']).reset_index()
            df_genres.rename(columns={'index': 'Genre'}, inplace=True)
            df_genres=df_genres[df_genres['Genre']!="(no genres listed)"]
            if len(df_genres)>=20:
               top=20
               df_genres=df_genres.nlargest(20,'Count')
            else:
               top=len(df_genres)
               df_genres=df_genres.nlargest(len(df_genres),'Count')
            df_genres['Count']=df_genres['Count'].astype('int32')
            df_genres = df_genres.set_index('Genre')
    recommended_movies = sim_knn.recomendacion_knn_old_user(selected_user_id)#recomendacion_knn_old_user
    if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(num_movies))
            lista_originalTitle = list(recommended_movies['title'].head(num_movies))
            lista_tconst = list(recommended_movies['imdb_id'].head(num_movies))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(num_movies))
            lista_years = list(recommended_movies['year'].head(num_movies))
            ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating,lista_years)
            # with st.expander("View Top 10 Genres chosen by him user"):
               #  st.write(df_genres.to_html(index=False), unsafe_allow_html=True)
               #  st.write(df_genres.to_html(index=False), unsafe_allow_html=True)
            st.markdown("""<hr style="height:10px;margin-top:15px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
            st.write(f'Top {top} - Genres with the most user votes!')
            st.dataframe(df_genres.T)