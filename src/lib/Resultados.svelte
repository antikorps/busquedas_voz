<script lang="ts">
    import type { ResultadosBusqueda } from "../modelos";

    export let resultadosBusqueda: ResultadosBusqueda;
</script>

{#if resultadosBusqueda.BusquedaRealizada}
    <h3>Resultados:</h3>

    {#if resultadosBusqueda.Coincidencias.length == 0 && resultadosBusqueda.Similitudes.length == 0}
    <p id="no-coincidencias">no se han encontrado coincidencias</p>
    {/if}

    {#if resultadosBusqueda.Coincidencias.length > 0}
        {#each resultadosBusqueda.Coincidencias as coincidencia}
            <article>
                {#if coincidencia.poster != null}
                    <img class="poster" src={"https://images.justwatch.com" + coincidencia.poster.replace("{profile}", "s166").replace("{format}", ".webp") || ""} alt="Pośter">
                {/if}
                
                <h3 class="titulo">{coincidencia.titulo} {coincidencia.lanzamiento != null ? " (" + coincidencia.lanzamiento.split("-")[0] + ")": ""}</h3>
                <p><strong>Título original</strong>: {coincidencia.titulo_original || ""}</p>
                <p><strong>Plataforma</strong>: {coincidencia.plataforma}</p>
                <p><strong>Tipo</strong>: {coincidencia.tipo.toUpperCase()}
                    {#if coincidencia.temporadas != null}
                    - <strong>Temporadas</strong>: {coincidencia.temporadas}
                    {/if}
                </p>
                <p><strong>Género</strong>: {coincidencia.generos.join(", ")}</p>
                <p><strong>Sinopsis</strong>: {coincidencia.sinopsis}</p>
                <p><strong>Duración</strong>: {coincidencia.duracion} minutos</p>
                {#if coincidencia.lanzamiento != null}
                    <p><strong>Lanzamiento</strong>: {coincidencia.lanzamiento}</p>
                {/if}

                {#if coincidencia.puntuacion_imdb != null}
                    <p><strong>IMDB</strong>: {coincidencia.puntuacion_imdb}</p>
                {/if}
                {#if coincidencia.puntuacion_tmdb != null}
                    <p><strong>TMDB</strong>: {coincidencia.puntuacion_tmdb}</p>
                {/if}
                <p><strong>Estrenada</strong>: {coincidencia.estreno ? "Sí" : "No"}</p>
            </article>
        {/each}
    {/if}


    {#if resultadosBusqueda.Similitudes.length > 0}
        <p id="solo-similitudes">no se ha encontradon coincidencias exatactas, ¿quiźa te referías a alguna de estas?</p>
        {#each resultadosBusqueda.Similitudes as similitud}
        <details>
            <!-- svelte-ignore a11y-no-redundant-roles -->
            <summary role="button">{similitud.titulo} {similitud.lanzamiento != null ? " (" + similitud.lanzamiento.split("-")[0] + ")": ""} - Probabilidad: {similitud.similitud.toFixed(2)}% -</summary>
            {#if similitud.poster != null}
            <img class="poster" src={"https://images.justwatch.com" + similitud.poster.replace("{profile}", "s166").replace("{format}", ".webp") || ""} alt="Pośter">
            <p><strong>Título original</strong>: {similitud.titulo_original || ""}</p>
            <p><strong>Plataforma</strong>: {similitud.plataforma}</p>
                <p><strong>Tipo</strong>: {similitud.tipo.toUpperCase()}
                    {#if similitud.temporadas != null}
                    - <strong>Temporadas</strong>: {similitud.temporadas}
                    {/if}
                </p>
                <p><strong>Género</strong>: {similitud.generos.join(", ")}</p>
                <p><strong>Sinopsis</strong>: {similitud.sinopsis}</p>
                <p><strong>Duración</strong>: {similitud.duracion} minutos</p>
                {#if similitud.lanzamiento != null}
                    <p><strong>Lanzamiento</strong>: {similitud.lanzamiento}</p>
                {/if}

                {#if similitud.puntuacion_imdb != null}
                    <p><strong>IMDB</strong>: {similitud.puntuacion_imdb}</p>
                {/if}
                {#if similitud.puntuacion_tmdb != null}
                    <p><strong>TMDB</strong>: {similitud.puntuacion_tmdb}</p>
                {/if}
                <p><strong>Estrenada</strong>: {similitud.estreno ? "Sí" : "No"}</p>
        {/if}
        </details>
        {/each}
    {/if}
    
{/if}

<style>
    #no-coincidencias {
        text-align: center;
        font-weight: 600;
        font-family: monospace;
        background: tomato;
        color: white;
        border-radius: 10px;
        padding: 10px 5px 10px 5px;
    }
    #solo-similitudes {
        text-align: center;
        font-weight: 600;
        font-family: monospace;
        background: orange;
        color: white;
        border-radius: 10px;
        padding: 10px 5px 10px 5px;
    }
    .poster {
        float:left;
        margin: 0 20px 20px 20px;
    }
    .titulo {
        text-align: center;
    }
</style>