import sqlite3
import json
from pathlib import Path

ruta_raiz = Path(__file__).parent
ruta_base_datos = ruta_raiz / "resultados_1681661758.sqlite3"
ruta_resultados_json = ruta_raiz / "resultados.json"

conexion = sqlite3.connect(ruta_base_datos)
cursor = conexion.cursor()

consulta = "SELECT * FROM registros WHERE titulo LIKE 'C%'"
cursor.execute(consulta)
registros = cursor.fetchall()

peliculas = []

for registro in registros:
    plataforma = registro[1]
    titulo = registro[2]
    titulo_original = registro[3]
    tipo = registro[4]
    justwatch_url = registro[5]
    try:
        generos = json.loads(registro[6])
    except:
        generos = None
    sinopsis = registro[7]
    try:
        duracion = int(registro[8])
    except:
        duracion = None
    lanzamiento = registro[9]
    try:
        creditos = json.loads(registro[10])
    except:
        creditos = None
    try:
        puntuacion_imdb = float(registro[11])
    except:
        puntuacion_imdb = None
    try:
        puntuacion_tmdb = float(registro[12])
    except:
        puntuacion_tmdb = None

    poster = registro[13]

    if registro[14] == 1:
        estreno = True
    else:
        estreno = False

    try:
        temporadas = int(registro[15])
    except:
        temporadas = None

    info_registro = {
        "plataforma": plataforma,
        "titulo": titulo,
        "titulo_original": titulo_original,
        "tipo": tipo,
        "justwatch_url": justwatch_url,
        "generos": generos,
        "sinopsis": sinopsis,
        "duracion": duracion,
        "lanzamiento": lanzamiento,
        "creditos":creditos,
        "puntuacion_imdb": puntuacion_imdb,
        "puntuacion_tmdb": puntuacion_tmdb,
        "poster":poster,
        "estreno": estreno,
        "temporadas": temporadas
    }
    peliculas.append(info_registro)
    
with open(ruta_resultados_json, "w+", encoding="UTF-8") as manejador:
    json.dump(peliculas, manejador)
