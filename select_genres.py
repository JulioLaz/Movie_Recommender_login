import ddbb
import title_poster_genre as tpg
import ver_poster

df_movies = ddbb.df_merge_movies_ratings()
num_movies=8

def select_genres(menu_id):
    tpg.title_poster_genre(menu_id,'Genre')
    df_genre = df_movies[df_movies['genres'] == menu_id].sort_values(by='rating', ascending=False)
    lista_poster = list(df_genre['poster_path_full'].head(num_movies))
    lista_originalTitle = list(df_genre['title'].head(num_movies))
    lista_tconst = list(df_genre['imdb_id'].head(num_movies))
    lista_averageRating = list(round(df_genre['rating'],1).head(num_movies))
    lista_years = list(df_genre['year'])
    ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating,lista_years)