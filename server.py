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
        if 'full_title' in output['response']['hits'][i]['result'].keys():
            song = output['response']['hits'][i]['result']['full_title']
        else:
            song = "No especificado"
        if 'header_image_url' in output['response']['hits'][i]['result'].keys():
            imag = output['response']['hits'][i]['result']['header_image_url']
        else:
            imag = "No especificado"
        pareja = [song, imag]
        solucion.append(pareja)
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

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error('Page not found: %s', (request.path))
    return render_template('error_404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

