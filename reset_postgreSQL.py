from sqlalchemy import create_engine, text
import pandas as pd
import streamlit as st

def crear_conexion():
    df = pd.read_csv('user_ratings.csv', names=['userId', 'movieId', 'title', 'rating', 'timestamp'], header=0)
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Conexión establecida con éxito!")
        df.columns = ['userId', 'movieId', 'title', 'rating', 'timestamp']
        df.to_sql('ratings', engine, if_exists='append', index=False)

        print("¡Datos guardados en la base de datos!")
    except Exception as e:
        print(f"Error al conectar o guardar los datos: {str(e)}")

def borrar_todas_las_filas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            print("Conexión establecida con éxito!")
            
            # Iniciar una transacción
            trans = connection.begin()
            try:
                # Ejecutar la instrucción SQL para borrar todas las filas
                connection.execute(text("DELETE FROM ratings"))
                # Confirmar la transacción
                trans.commit()
                print("¡Todas las filas han sido borradas de la tabla: ratings!")
            except Exception as e:
                # Revertir la transacción en caso de error
                trans.rollback()
                print(f"Error al borrar las filas: {str(e)}")
    
    except Exception as e:
        print(f"Error al conectar: {str(e)}")

from sqlalchemy import create_engine, inspect

def obtener_nombres_de_tablas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)

        # Obtener los nombres de todas las tablas en la base de datos
        nombres_de_tablas = inspector.get_table_names()

        if nombres_de_tablas:
            print("Tablas en la base de datos:")
            for nombre in nombres_de_tablas:
                print(nombre)
        else:
            print("No se encontraron tablas en la base de datos.")
    
    except Exception as e:
        print(f"Error al conectar o al obtener los nombres de las tablas: {str(e)}")


from sqlalchemy import create_engine, MetaData

def borrar_todas_las_tablas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        meta = MetaData()  # No se usa 'bind' aquí
        meta.reflect(bind=engine)  # Se pasa 'engine' al reflejar las tablas

        # Borrar todas las tablas
        meta.drop_all(bind=engine)
        print("¡Todas las tablas han sido eliminadas!")

    except Exception as e:
        print(f"Error al borrar las tablas: {str(e)}")

def obtener_nombres_y_estructuras_de_tablas():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)

        # Obtener los nombres de todas las tablas en la base de datos
        nombres_de_tablas = inspector.get_table_names()

        if nombres_de_tablas:
            print("Tablas en la base de datos:")
            for nombre in nombres_de_tablas:
                print(f"\nTabla: {nombre}")
                # Obtener la estructura de la tabla
                columnas = inspector.get_columns(nombre)
                for columna in columnas:
                    print(f"Columna: {columna['name']}, Tipo: {columna['type']}")
        else:
            print("No se encontraron tablas en la base de datos.")
    
    except Exception as e:
        print(f"Error al conectar o al obtener los nombres de las tablas: {str(e)}")


from sqlalchemy import create_engine, text
import streamlit as st

def limpiar_ddbb_postgres():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    engine = create_engine(DATABASE_URL)

    try:
        with engine.connect() as connection:
            # SQL query to delete duplicates and keep the row with the latest timestamp
            query = text("""
            DELETE FROM ratings
            WHERE ctid IN (
                SELECT ctid
                FROM (
                    SELECT ctid,
                           ROW_NUMBER() OVER (PARTITION BY "userId", "movieId" ORDER BY "timestamp" DESC) as row_num
                    FROM ratings
                ) as subquery
                WHERE row_num > 1
            );
            """)
            connection.execute(query)
            print("Duplicated rows deleted successfully, keeping the latest entry!")
    except Exception as e:
        print(f"Error while deleting duplicates: {str(e)}")

# limpiar_ddbb_postgres()



# obtener_nombres_y_estructuras_de_tablas()

# crear_conexion()
# borrar_todas_las_tablas()
borrar_todas_las_filas()
# obtener_nombres_de_tablas()