import requests
from io import BytesIO
import streamlit as st
from PIL import Image
import star_score_rating as ssr
import ddbb

API_KEY = st.secrets["KEY"]

df_links=ddbb.load_df_links()

@st.cache_data(ttl=300)
def obtener_info_pelicula(imdb_id):
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
    
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

def view_movie_details(imdb_id):
    movieId=df_links[df_links['imdbId']==imdb_id]['movieId']
    movieId=movieId.values[0]
    details = obtener_info_pelicula(imdb_id)
    if details:
        st.write(f"""<h2 style="color: gold; font-size: 2rem; height: 2.5rem; text-align: center; padding: 0px;margin-bottom:15px">
               {details["titulo"]}
               </h2>""", unsafe_allow_html=True)
        # st.subheader(details["titulo"])
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(load_image_from_url(details["poster_url"]), use_column_width=True)
        with col2:
            st.write(f"📅 **Año:** {details['Released']}")
            st.write(f"🎬 **Director:** {details['director']}")
            st.write(f"🎭 **Actor:** {details['Actors']}")
            st.write(f"⏱️ **Duración:** {details['Runtime']}")
            st.write(f"🏅 **Premios:** {details['Awards']}") 
            st.write(f"💰 **Box Office:** {details['BoxOffice']}")
           
        st.subheader("**Descripción:**")
        st.write(details['descripcion'])
        # st.write(type(movieId))
    else:
        st.sidebar.error("No se pudo obtener la información de la película.")
    ssr.rate_with_stars(movieId,'W')

def view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating,lista_years):
    num_posters = len(lista_poster)
    # print('0'*20)
    # print('num_posters: ',num_posters)
    # print('0'*20)
    num_rows = (num_posters + 7) // 8  # Calculate number of rows (ceiling division)

    for row in range(num_rows):
        cols = st.columns(8)  # Always create 8 columns
        start_index = row * 8
        end_index = min(start_index + 8, num_posters)

        for i in range(start_index, end_index):
            col_index = i % 8
            with cols[col_index]:
                try:
                    image = load_image_from_url(f"https://image.tmdb.org/t/p/w500{lista_poster[i]}")
                    st.image(image, use_column_width=True)
                    st.markdown(
                        f"""
                        <div style="background-color:#0e1117;color:red;padding:2px 0px;text-align:center;font-size:calc(12px + .1vw);height:2rem;box-sizing:unset">
                            {lista_originalTitle[i][:17] + "..." if len(lista_originalTitle[i]) > 22 else lista_originalTitle[i]}
                        </div>
                        """, unsafe_allow_html=True
                    )
                    
                    st.markdown(
                        f"""
                        <div style="display:flex; justify-content: center;height:1.9rem;margin-bottom:15px;margin-top:3px;">
                            <div style="position: relative; top: -3rem;right:-1rem; background-color:rgba(0,0,0,.5);border:1px solid black; border-radius:4px;padding: 0 3px"><span style="font-size:10px">year</span>{int(lista_years[i])}</div>
                            <div style="background-color:none;font-weight:600;color:white;padding:0px;text-align:center;font-size:20px;font-weight:bold">
                            <span style="font-size:10px; padding-right:3px">rating</span>{lista_averageRating[i]}
                            </div>
                            <div style="background-color:#0e1117;color:#0e1117;padding:0px;text-align:end;font-size:calc(10px + .1vw)">
                                {"⭐" * min(int(float(lista_averageRating[i])), 5)}<br>
                                {"⭐" * (int(float(lista_averageRating[i])) - 5) if int(float(lista_averageRating[i])) > 5 else "."}
                            </div>
                        </div>
                        """, unsafe_allow_html=True
                    )


                except IndexError:
                    st.error(f"Index {i} out of range for the title list.")
                except Exception as e:
                    st.error(f"Error: {e}")

    if 'show_details' in st.session_state:
        st.sidebar.empty()
        with st.sidebar:
            st.sidebar.markdown(
                """
                <style>
                    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                        width: 40vw !important;
                        background-color: red;
                    }
                    @media (max-width: 768px) {
                        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
                            width: 100% !important;
                        }                    
                    /* wihdt sidebar */
                    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1i4v8s7.eczjsme18{
                     max-width: none !important;
                     width:40vw !important
                     }
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11{
                     max-width: none !important;
                     width:40vw !important                     }
                     /* sidebar */
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-16txtl3.eczjsme4{
                     padding: 1.5rem 1.5rem;}
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-16txtl3.eczjsme4 > div > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(2) > div > div > div > div:nth-child(1) > div > div > div > div > h1{
                     padding-top:0 !important;}
                     #root > div:nth-child(1) > div.withScreencast > div > div > div > section.st-emotion-cache-1ec6rqw.eczjsme11 > div.st-emotion-cache-6qob1r.eczjsme3 > div.st-emotion-cache-16txtl3.eczjsme4 > div > div > div > div > div.st-emotion-cache-ocqkz7.e1f1d6gn5 > div:nth-child(2) > div > div > div > div:nth-child(7) > div > div > p{
                     margin:0 !important}
                </style>
                """,
                unsafe_allow_html=True,
            )
            view_movie_details(st.session_state.show_details)