import populares as pop
import title_poster_genre as tpg
import ver_poster
num_movies=8

def most_populars():
    tpg.title_poster_genre('','Most popular movies among our users!')
    df=pop.recomendacion_populares()
    lista_poster = list(df['poster_path_full'].head(num_movies))
    lista_originalTitle = list(df['title'].head(num_movies))
    lista_tconst = list(df['imdb_id'].head(num_movies))
    lista_averageRating = list(round(df['mean_rating'],1).head(num_movies))
    lista_years = list(df['year'].head(num_movies))
    ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating,lista_years)