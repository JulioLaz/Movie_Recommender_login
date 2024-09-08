import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
import ddbb
import datetime
from sqlalchemy import create_engine

DATABASE_URL = st.secrets["DATABASE_URL"]
engine = create_engine(DATABASE_URL)

df = ddbb.df_final()
df_poster = ddbb.load_df_poster()
df = df.merge(df_poster, on='movieId', how='left')

def guardar_datos(df_ratings):
    DATABASE_URL = st.secrets["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)
    if not df_ratings.empty:
        df_ratings.to_sql('ratings', engine, if_exists='append', index=False)
        st.cache_data.clear()  # Clear the cache after saving data
        st.session_state.reload_data = True  # Set flag to reload data
      #   st.experimental_rerun()  # Rerun the app to reflect the updates
    else:
        print("No data to save.")

# def guardar_datos(df_ratings):
#     DATABASE_URL = st.secrets["DATABASE_URL"]
#     engine = create_engine(DATABASE_URL)
#     if not df_ratings.empty:
#         df_ratings.to_sql('ratings', engine, if_exists='append', index=False)
#         st.cache_data.clear()  # Clear the cache after saving data
#     else:
#         print("No data to save.")


def rate_with_stars(movie_ids,color):
      global df_ratings 
      df_ratings = pd.DataFrame(columns=["userId", "movieId", "title", "rating","timestamp"])

      # userId = st.number_input("Enter your user ID", min_value=df.userId.max()+1, step=1)
      userId= st.session_state.get("user_id")
      # if userId in df["userId"].unique() or userId in df_ratings["userId"].unique():
      if userId:
         st.write("""<h2 style="color: gold; font-size: 1.4rem; height: 2.5rem; text-align: center; padding: 0px;margin-top:10px">
               How many stars for this film?
               </h2>""", unsafe_allow_html=True)
         def calificar(df_details, userId):
            calificaciones = []
            for index, row in df_details.iterrows():
               if color == 'R':
                  rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}",
                           customCSS = "div {background-color: red;border:none;display: flex;justify-content: center; align-items: center;height: 4.5rem;padding-top: 3px;width: 100%},h3 {display: none}, #root > div > ul {display: flex;justify-content: center;}")
               else:
                  rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}_{userId}",
                  # rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}",
                           customCSS = "div {background-color: rgb(14, 17, 23);border:none;display: flex;justify-content: center; align-items: center;height: 4.5rem;padding-top: 3px;width: 100%},h3 {display: none}, #root > div > ul {display: flex;justify-content: center;}")
               if rating > 0:
                     # calificaciones.append({'userId': userId, 'movieId': row['movieId'], 'title': row['title'], 'rating': rating})
                                     calificaciones.append({
                    'userId': userId, 
                    'movieId': row['movieId'], 
                    'title': row['title'], 
                    'rating': rating,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            if calificaciones:
                  new_df_ratings = pd.DataFrame(calificaciones)
                  global df_ratings
                  df_ratings = pd.concat([df_ratings, new_df_ratings], ignore_index=True)

         # Function to extract movie details by movieId
         def dicc(movieId):
            global df
            movie_data = df[df['movieId'] == movieId]
            if movie_data.empty:
                  return None
            return {
                  'movieId': movie_data.movieId.iloc[0],
                  'title': movie_data.title.iloc[0],
                  'poster_path_full': movie_data.poster_path_full.iloc[0],
                  'year': movie_data.year.iloc[0],
                  'genres': movie_data.genres.iloc[0],
                  'rating': movie_data.rating.iloc[0]
            }

         # Function to create a DataFrame with movie details
         def crear_dataframe_con_detalles(movie_ids):
            movie_details = []
            for movieId in movie_ids:
                  details = dicc(movieId)
                  if details:
                     movie_details.append(details)
            
            df_details = pd.DataFrame(movie_details)
            return df_details

         df_details = crear_dataframe_con_detalles([movie_ids])
         calificar(df_details, userId)
         guardar_datos(df_ratings)
      else:
               st.write("""<h2 style="color: gold; font-size: 1.4rem; height: 3rem; text-align: center; padding: 0px;margin-top:10px">
               Login to rate your movie now!
               </h2>""", unsafe_allow_html=True)
               st.markdown("""
                  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                  """, unsafe_allow_html=True)

               # Mostrar las estrellas centradas
               st.markdown("""
                  <div style="text-align: center;">
                     <i class="fa fa-star" style="font-size: 3rem; color: #f5f5f5;"></i>
                     <i class="fa fa-star" style="font-size: 3rem; color: #f5f5f5;"></i>
                     <i class="fa fa-star" style="font-size: 3rem; color: #f5f5f5;"></i>
                     <i class="fa fa-star" style="font-size: 3rem; color: #f5f5f5;"></i>
                     <i class="fa fa-star" style="font-size: 3rem; color: #f5f5f5;"></i>
                  </div>
                  """, unsafe_allow_html=True)
      