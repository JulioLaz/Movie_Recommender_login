import requests
from io import BytesIO
import streamlit as st
from PIL import Image
import star_score_rating as ssr
import ddbb
# load_dotenv()  # Carga las variables del archivo .env
# API_KEY = os.getenv("KEY")
API_KEY = st.secrets["KEY"]

df_links=ddbb.load_df_links()

@st.cache_data(ttl=300)
def obtener_info_pelicula_new_use(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    # print('data response: ', data)
    if data["Response"] == "True":
        return {
            "titulo": data["Title"],
            "descripcion": data["Plot"],
            "poster_url": data["Poster"],
            "director": data["Director"],
            "Actors": data["Actors"],
            "Runtime": data["Runtime"],
            "Awards": data["Awards"],
            "Released": data["Released"],
            "BoxOffice": data["BoxOffice"],
        }
    else:
        return None

def load_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img



def view_movie_details_new_user(imdb_id,lista_averageRating):
    movieId = df_links[df_links['imdbId'] == imdb_id]['movieId']
    movieId = movieId.values[0]
    details = obtener_info_pelicula_new_use(imdb_id)
    if details:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            # Adjusting the image size and alignment
            st.markdown(
                f"""
                <div style="height: 65vh; display: flex; align-items: center; justify-content: flex-end;margin-bottom:1rem">
                    <img src="{details['poster_url']}" style=" border-radius: 10px;height: 65vh">
                </div>
                """, 
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div style="height: 65vh;width:45vw; display: flex; flex-direction: column; justify-content: center; padding:0 1rem; border-radius: 10px; background-color: black;margin-bottom:1rem">
                    <h2 style="color: gold; font-size: 2rem; text-align: center; margin-bottom: 15px;padding:0px !important">
                        {details['titulo']}
                    </h2>
                    <p>📅 <strong>Año:</strong> {details['Released']}</p>
                    <p>🎬 <strong>Director:</strong> {details['director']}</p>
                    <p>🎭 <strong>Actores:</strong> {details['Actors']}</p>
                    <p>⏱️ <strong>Duración:</strong> {details['Runtime']}</p>
                    <p>🏅 <strong>Premios:</strong> {details['Awards']}</p> 
                    <p>💰 <strong>Box Office:</strong> {details['BoxOffice']}</p>
                    <h4>Descripción:</h4>
                    <p>{details['descripcion']}</p>
                    <div style="background-color:#000;color:white;padding:0px;text-align:center;font-size:calc(12px + .1vw)">
                        rating {lista_averageRating} {"⭐" * min(int(float(lista_averageRating)), 5)}<br>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                        # {"⭐" * (int(float(lista_averageRating)) - 5) if int(float(lista_averageRating)) > 5 else "."}
    else:
        st.sidebar.error("No se pudo obtener la información de la película.")
    ssr.rate_with_stars(movieId, 'W')

def view_poster_new_user(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating,lista_years):
    if not lista_poster:
        st.error("No hay pósters disponibles para mostrar.")
        return
    i = 0
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; width: 100%;flex-direction:row">
            <div style="width: 22vw;">
                <img src="https://image.tmdb.org/t/p/w500{lista_poster[i]}" style="width: 100%; height: auto;">
                <div style="background-color:none;font-weight:600;color:red;padding:2px 0px;text-align:center;font-size:calc(12px + .1vw);height:2rem;">
                    {lista_originalTitle[i][:30] + "..." if len(lista_originalTitle[i]) > 35 else lista_originalTitle[i]}
                </div>
                <div style="display:flex; justify-content: center;height:1.9rem;margin-top:3px;">
                    <div style="position: relative; top: -5rem;right:-2rem; background-color:rgba(0,0,0,.5);border:1px solid black; border-radius:4px;padding: 0 3px"><span style="font-size:10px">year</span>{int(lista_years[i])}</div>
                    <div style="background-color:#0e1117;color:white;padding:0px;text-align:center;font-size:20px;font-weight:bold">
                        <span style="font-size:10px; padding-right:3px">rating</span>{lista_averageRating[i]}
                    </div>
                    <div style="background-color:#0e1117;color:#0e1117;padding:0px;text-align:end;font-size:calc(10px + .1vw)">
                        {"⭐" * min(int(float(lista_averageRating[i])), 5)}<br>
                        {"⭐" * (int(float(lista_averageRating[i])) - 5) if int(float(lista_averageRating[i])) > 5 else "."}
                    </div>
                </div>
            </div>
            <div>{view_movie_details_new_user(lista_tconst[i])}</div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Trailer', key=f'btn_trailer_{i}'):
            video_url = f"https://www.imdb.com/title/{lista_tconst[i]}/"
            st.write(f"[Ver en IMDb]({video_url})")
    with col2:
        if st.button('Details', key=f'btn_details_{i}'):
            st.session_state.show_details = lista_tconst[i]

    if 'show_details' in st.session_state:
        st.sidebar.empty()
        with st.sidebar:
            # (El código del sidebar se mantiene igual)
            view_movie_details_new_user(st.session_state.show_details)