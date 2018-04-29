# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import http.client
import json
from flask import render_template, url_for, redirect

def buscadorApi(url):
    web = "api.genius.com"
    accestoken = 'PIXypyIkP4sT8Kvz8TC_0e3CcvoI9p_tIHW0LmwMbDhh3V8k_FmLq5K1nPBoiUXH'
    headers = {'User-Agent': 'http-client', 'Authorization': 'Bearer {}'.format(accestoken)}
    print(web + url)

    conexion = http.client.HTTPSConnection(web)
    try:
        conexion.request("GET", url, None, headers)
    except http.client.socket.gaierror as error:
        print(error)
        print("Error de conexión, la URL {} no existe".format(web))
        code = "Error"
        return code

    response = conexion.getresponse()
    if response.status != 200:
        print("Error de conexión, el recurso solicitado {} no existe".format(url))
        code = "Error"
        return code

    data = response.read().decode("utf-8")
    conexion.close()
    output = json.loads(data)
    return output

def searchArtist(output):
    solucion = []

    for i in range(len(output['response']['hits'])):
        song = output['response']['hits'][i]['result']['full_title']
        imag = output['response']['hits'][i]['result']['song_art_image_thumbnail_url']
        link_song = output['response']['hits'][i]['result']['id']
        link = 'http://127.0.0.1:8000/song?id={}'.format(link_song)
        pareja = [song, imag, link]
        solucion.append(pareja)
    return solucion

def searchSong(output):
    song = output['response']['song']['full_title']
    imag = output['response']['song']['song_art_image_thumbnail_url']
    autor = output['response']['song']['album']['artist']['name']
    album = output['response']['song']['album']['name']
    autor = output['response']['song']['album']['artist']['name']
    try:
        for i in range(len(output['response']['song']['media'])):
            if 'native_uri' in output['response']['song']['media'][i].keys():
                print(spotify_uri)
                spotify_uri = output['response']['song']['media'][i]['native_uri']

                break
            else:
                spotify_uri= "No disponible"
    except:
        spotify_uri = "Unkwnow"
    spotify = "https://embed.spotify.com/?uri={}".format(spotify_uri)
    solucion=[song, imag, spotify, autor, album]
    print(solucion)
    return solucion

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def getInicio():
    return render_template("inicio.html")

@app.route('/searchSongs', methods=['GET'])
def getArtist():
    artist = request.args.get('artist', default = "*", type = str)
    artist_search = artist.replace(" ","+")
    datos = buscadorApi('/search?q={}'.format(artist_search))
    if datos == "Error":
        return render_template("error.html")
    message = searchArtist(datos)
    print(message)
    return render_template("search_artist.html", content = message, artist_name = artist)

@app.route('/song', methods=['GET'])
def getSong():
    song = request.args.get('id', default = "*", type = int)
    datos = buscadorApi('/songs/{}'.format(song))
    if datos == "Error":
        return render_template("error.html")
    message = searchSong(datos)
    print(message)
    return render_template("search_song.html", content = message, artist_name = message[0], spotify_link = message[2])

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found: %s', (request.path))
    return render_template('error_404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

