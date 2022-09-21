from flask import Flask, request, redirect, session
from flask_cors import CORS
import requests
import deezer
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from keras.models import Model

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app)

client = deezer.Client()

BATCH_SIZE = 4
NUM_EP = 5

#### Leer los datos
full_data_df = pd.read_csv("data.csv")

# Parte de los usuarios
users_df = pd.DataFrame()
users_df[["user", "user_id"]] = full_data_df[["user", "user_id"]]
users_df = users_df.drop_duplicates(ignore_index = True)

# Parte de las canciones
data_df = pd.DataFrame()
data_df[["song", "song_id", "full_name", "title", "artist", "album", "duration", "release_date"]] = full_data_df[["song",
                    "song_id", "full_name", "title", "artist", "album", "duration", "release_date"]]
data_df["genres"] = full_data_df.genres.str.split("-")
data_df = data_df.sort_values("release_date").drop_duplicates(subset=["song"], ignore_index = True)


def get_recommendations(songs1, songs2, user):
    """
    Devuelve un JSON con las 10 canciones que se le recomienda al usuario
    """

    songs_df1 = pd.DataFrame(songs1)
    songs_df1["like"] = 1

    songs_df2 = pd.DataFrame(songs2)
    songs_df2["like"] = 0.5

    songs_user_df = pd.concat([songs_df1, songs_df2], ignore_index=True)
    songs_user_df["full_name"] = songs_user_df["title"] + " - " + songs_user_df["artist"]
    songs_user_df = songs_user_df.drop_duplicates(subset=["full_name"])
    songs_user_df["user"] = user

    songs_user_df["like"] = songs_user_df["like"].values.astype(np.float32)

    # Carga el modelo
    model = keras.models.load_model("model.h5")

    # Entrenar el modelo con los datos del usuario nuevo   
    model.fit([songs_user_df["user"], songs_user_df["song"]], songs_user_df["like"], epochs=NUM_EP, verbose=1, batch_size=BATCH_SIZE)

    # Filtrar candidatas
    songs_not_listened = filtrar_candidatos(songs_user_df)

    # array con los ids de todas las canciones no escuchadas
    songs_np = np.array(list(set(songs_not_listened.song)))

    # array con el usuario
    user_np = np.array([user for i in range(len(songs_np))])

    # Hacer predicciones:
    ratings = model.predict([user_np, songs_np]).flatten()

    top_ratings_indices = ratings.argsort()[-10:][::-1]

    recommended_songs_ids = [songs_not_listened.iloc[x][0] for x in top_ratings_indices]

    return songsids_to_json(recommended_songs_ids)



def songsids_to_json(recommended_songs_ids):
    """
    Función que recibe una lista de canciones y la devuelve como JSON.
    """
    songs_json = []
    recommended_songs = data_df[data_df["song"].isin(recommended_songs_ids)]

    for i in range(recommended_songs.shape[0]):

        song_id = int(recommended_songs["song_id"].values[i])
        song = int(recommended_songs["song"].values[i])
        title = recommended_songs["title"].values[i]
        artist = recommended_songs["artist"].values[i]
        release = recommended_songs["release_date"].values[i]
        genres = recommended_songs["genres"].values[i]

        cancion = None
                    
        while cancion == None:
            try:
                cancion = client.get_track(str(song_id))
            except Exception as error:
                if len(error.args[0]) == 1 and error.args[0]["error"]["type"] == "Exception":
                    # Espera por el limite de consultas
                    time.sleep(0.01)
                else:                    
                    # no se puede obtener informacion de la cancion
                    cancion = song_id

        try:
        # Obtiene la imagen de portada del album
            cover = cancion.album.cover_medium
        except:
            cover = "http://cdn.onlinewebfonts.com/svg/img_296254.png"


        song_data = {
            "id": song_id,
            "song": song,
            "title": title,
            "artist": artist,
            "release_date": release,
            "genres": genres,
            "cover": cover
        }

        songs_json.append(song_data)
    
    return songs_json


def get_genre_fav(genres_list):
    """
    Devuelve el genero favorito dado un listado.
    """

    list_genres = []
    list_count = []
    for genre_song in genres_list:
        for genre in genre_song:
            if genre not in list_genres:
                list_genres.append(genre)
                list_count.append(1)
            else:
                index = list_genres.index(genre)
                list_count[index] = list_count[index]+1

    index = list_count.index(max(list_count))
    genre_fav = list_genres[index]

    return genre_fav


def get_min_max_date(dates_list):
    """
    Devuelve el año minimo y maximo
    """
    # Calcular cancion mas antigua y añadir un año de margen
    min_date = min(dates_list)
    min_year = str(int(min_date[:4]) - 1)

    # Calcular cancion mas actual y añadir un año de margen
    max_date = max(dates_list)
    max_year = str(int(max_date[:4]) + 1)

    return min_year, max_year


def filtrar_candidatos(songs_user_df):
    """
    Devuelve los candidatos tras aplicar un filtrado basado en contenido
    """
    # Filtrar por genero favorito
    genre_fav = get_genre_fav(songs_user_df["genres"])
    songs_genres_liked = data_df[pd.DataFrame(data_df.genres.tolist()).isin([genre_fav]).any(1).values].drop_duplicates("song")

    # Filtrar por fecha de salida
    min_year, max_year = get_min_max_date(songs_user_df["release_date"])

    song_dates_filter = songs_genres_liked[songs_genres_liked["release_date"] >= min_year]
    song_dates_filter = song_dates_filter[song_dates_filter["release_date"] <= max_year]

    # Eliminar las canciones ya escuchadas
    songs_not_listened = song_dates_filter[~song_dates_filter["song"].isin(songs_user_df.song.values)][["song"]].drop_duplicates()

    return songs_not_listened


def songs_to_json(songs):
    """
    Función que recibe un listado de canciones y las devuelve en formato JSON
    """
    songs_json = []
    for s in songs:

        fullname = s.title + " - " + s.artist.name

        if fullname in data_df["full_name"].values:
            
            # obtiene todos los datos de la cancion
            cancion = None
            while cancion == None:
                try:
                    cancion = client.get_track(str(s.id))
                except Exception as error:
                    if len(error.args[0]) == 1 and error.args[0]["error"]["type"] == "Exception":
                        # Espera por el limite de consultas
                        time.sleep(0.01)
                    else:                    
                        # no se puede obtener informacion de la cancion
                        cancion = 0
            
            try:
                # Obtiene la imagen de portada del album
                cover = cancion.album.cover_medium
            except:
                cover = "http://cdn.onlinewebfonts.com/svg/img_296254.png"


            data_song = data_df[data_df["full_name"] == fullname]

            song = int(data_song["song"].values[0])
            genres = data_song["genres"].values[0]
            release = data_song["release_date"].values[0]

            song_data = {
                "id": s.id,
                "song": song,
                "title": s.title,
                "artist": s.artist.name,
                "release_date": release,
                "genres": genres,
                "cover": cover
            }

            songs_json.append(song_data)
    
    return songs_json



@app.route("/usuario/<id>", methods = ["GET"])
def get_user_songs(id):
    """
    GET: recibe el id de un usuario y devuelve sus datos, canciones y recomendaciones
    """
    if request.method == 'GET':

        try:

            usuario = client.get_user(id)

            user_id = int(id)

            if user_id in users_df["user_id"].values:
                # ya esta codificado previamente
                user = int(users_df[users_df["user_id"] == user_id]["user"].values[0])
            else:
                user = max(users_df["user"])+1

            try:
                # Obtiene el chart del usuario
                songs_chart = songs_to_json(client.request("GET", "user/"+str(id)+"/charts/tracks"))
            except:
                songs_chart = []

            try:
                # Obtiene las canciones guardadas del usuario, hasta 50
                songs_fav = songs_to_json(client.get_user_tracks(id)[:50])
            except:
                songs_fav = []
            
            try:
                # Obtiene el nombre del usuario
                user_name = usuario.name
            except:
                user_name = "unknown"
            
            try:
                # Obtiene el pais del usuario
                user_country = usuario.country
            except:
                user_country = "unknown"

            try:
                # Obtiene la foto de perfil del usuario
                user_picture = usuario.picture_medium
            except:
                user_picture = "https://cdn.icon-icons.com/icons2/936/PNG/512/user-shape_icon-icons.com_73346.png"  
            
            # Genera recomendaciones
            recommendations = get_recommendations(songs_chart, songs_fav, user)

            data = {
                "user" : user,
                "user_id" : user_id,
                "name" : user_name,
                "country" : user_country,
                "picture" : user_picture,
                "songs_chart" : songs_chart,
                "songs_fav" : songs_fav,
                "recommendations" : recommendations
            }

            return data

        except:
            return "400: BAD INPUT."

    else:
        return "400: BAD REQUEST."


@app.route('/')
def default():
    return "Hola mundo"
