import ddbb
import ast
import pandas as pd
import requests
import streamlit as st

df_final=ddbb.df_final()
df_links=ddbb.load_df_links()
df_sorted = df_final.sort_values(by=['year', 'rating'], ascending=[False, False])

def get_last_years(genre):
   df_filtered = df_sorted[df_sorted['rating'] > 4.5]
   df_filtered=df_filtered.drop_duplicates(subset=['userId',])
   df_filtered=df_filtered.drop_duplicates(subset=['movieId'])
   df_filtered=df_filtered.nlargest(1000,'year')
   df_last_years_links=df_filtered.merge(df_links, on='movieId', how='left')
   df_last_years_links = df_last_years_links.explode('genre_set')
   columnas=['movieId','rating','title','genre_set','year','imdbId']
   #fitrar por la columna genres_set:
   df_last_years_links = df_last_years_links[df_last_years_links['genre_set'].str.contains(genre)] 
   df_last_years_links=df_last_years_links[columnas]

# print(df_last_years_links)