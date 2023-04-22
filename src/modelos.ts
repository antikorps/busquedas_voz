interface Resultado {
    plataforma: string;
    titulo: string;
    titulo_original: string;
    tipo: string;
    justwatch_url: string;
    generos: string[];
    sinopsis: string;
    duracion: number;
    lanzamiento?: string;
    creditos: Credito[];
    puntuacion_imdb?: number;
    puntuacion_tmdb?: number;
    poster?: string;
    estreno: boolean;
    temporadas?: number;
    similitud: number;
}

interface Credito {
    role: string;
    name: string;
    characterName: string;
    personId: number;
}

interface ResultadosBusqueda {
    BusquedaRealizada: boolean;
    Coincidencias: Resultado[],
    Similitudes: Resultado[]
}

export type {Resultado, ResultadosBusqueda}