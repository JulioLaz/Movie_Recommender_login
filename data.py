import pandas as pd
import streamlit as st
path_img = 'https://i0.wp.com/image.tmdb.org/t/p/w300'

@st.cache_data(ttl=600)
def data():
   file_id = '1-5ilztJwpEJf7MtlE3C4A1tR9MFtf6pk'
   url = f'https://drive.google.com/uc?export=download&id={file_id}'
   df = pd.read_csv(url)
   return df
# print(data().genres_x.unique())

@st.cache_data(ttl=300)
def data_genre_explode():
   df = data()
   df = df.explode('genres_x')
   df = df.dropna(subset=['poster_path'])
   df['poster_path_full'] = df['poster_path'].apply(lambda x: f"{path_img}{x}")
   return df

# print(len(data_genre_explode().tconst))