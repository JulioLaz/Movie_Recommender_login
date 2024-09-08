from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def extraer_datos():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        conn = engine.raw_connection()
        cur = conn.cursor()
        query_all = "SELECT * FROM ratings"
        cur.execute(query_all)
        rows = cur.fetchall()
        df_all = pd.DataFrame(rows, columns=['userId', 'movieId', 'title', 'rating', 'timestamp'])  # Especifica los nombres de las columnas
        return df_all
    except Exception as e:
        print(f"Error al conectar o extraer los datos: {str(e)}")
        return None

   
# df_completo = extraer_datos()
# print(df_completo)