import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import hydralit_components as hc

@st.cache_data(ttl=300)
def imagen_cloud(df, column):
  with hc.HyLoader('Espera un poco', hc.Loaders.standard_loaders, index=[5]):

    urls = df[column].dropna().unique()[:50]
    print(urls)
    images = []
    for url in urls:
        response = requests.get(f"https://image.tmdb.org/t/p/w500{url}")
        img = Image.open(BytesIO(response.content))
        img = img.resize((100, 180))  # Redimensionar a 3rem (1rem = 16px)
        images.append(img)

    canvas = Image.new('RGB', (1000, 1000), (0, 0, 0))

    x, y = 0, 0
    for img in images:
        canvas.paste(img, (x, y))
        x += img.width
        if x >= canvas.width:
            x = 0
            y += img.height
    
    st.image(canvas)

#aplicar el: with hc.HyLoader('Espera un poco',hc.Loaders.standard_loaders,index=[5]):
#hasta que termine de cargar las imagenes