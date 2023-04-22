<script lang="ts">
    import type { Resultado, ResultadosBusqueda } from "../modelos";

    export let resultadosBusqueda: ResultadosBusqueda;

    let recognitionDisponible: boolean;
    let busqueda: string;
    let realizandoBusqueda = false;
    let resultados: Resultado[] = [];
    
    let criteriosBusqueda = [
        {
            valor: "titulo",
            texto: "Título",
            seleccionado: true,
        },
        {
            valor: "titulo_original",
            texto: "Título original",
            seleccionado: false,
        },
    ];
    let criterioSeleccionado: string;

    let idioma = "es-ES";

    let recognition: any;
    try {
        recognition = new window.webkitSpeechRecognition();
        recognitionDisponible = true;
    } catch (exception) {
        recognitionDisponible = false;
    }

    function reconocimientoVoz() {
        recognition.continuous = false;
        recognition.lang = idioma;
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.start();

        recognition.onresult = (evento) => {
            try {
                busqueda = evento.results[0][0].transcript
                buscar()
            }
            catch(excepcion) {

            }
        };
    }

    function normalizarTexto(texto: string): string {
        return texto
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();
    }

    function levenshteinDistance(s1, s2): number {
        var array = new Array(s1.length + 1);
        for (var i = 0; i < s1.length + 1; i++)
            array[i] = new Array(s2.length + 1);

        for (var i = 0; i < s1.length + 1; i++) array[i][0] = i;
        for (var j = 0; j < s2.length + 1; j++) array[0][j] = j;

        for (var i = 1; i < s1.length + 1; i++) {
            for (var j = 1; j < s2.length + 1; j++) {
                if (s1[i - 1] == s2[j - 1]) array[i][j] = array[i - 1][j - 1];
                else {
                    array[i][j] = Math.min(
                        array[i][j - 1] + 1,
                        array[i - 1][j] + 1
                    );
                    array[i][j] = Math.min(
                        array[i][j],
                        array[i - 1][j - 1] + 1
                    );
                }
            }
        }
        return array[s1.length][s2.length];
    }

    function calcularSimilitud(s1: string, s2: string): number {
        var longer = s1;
        var shorter = s2;
        if (s1.length < s2.length) {
            longer = s2;
            shorter = s1;
        }
        var longerLength = longer.length;
        if (longerLength == 0) {
            return 1.0;
        }
        return (longerLength - levenshteinDistance(longer, shorter)) / longerLength;
    }

    async function buscar() {
        // Reseteo
        realizandoBusqueda = true;
        resultadosBusqueda = {
            BusquedaRealizada: false,
            Coincidencias: [],
            Similitudes: [],
        };

        // Petición
        if (resultados.length == 0) {
            const pet = await fetch("resultados.json");
            const respuesta = await pet.json();
            resultados = respuesta;
        }

        // Comprobación
        const busquedaNormalizada = normalizarTexto(busqueda);
        for (const res of resultados) {
            const tituloNormalizado = normalizarTexto(res.titulo);
            const tituloOriginalNormalizado = normalizarTexto(res.titulo_original);

            // Coincidencias
            if (criterioSeleccionado == "titulo") {
                if (busquedaNormalizada == tituloNormalizado) {
                    resultadosBusqueda.Coincidencias.push(res);
                    continue;
                }
            } else {
                if (busquedaNormalizada == tituloOriginalNormalizado) {
                    resultadosBusqueda.Coincidencias.push(res);
                    continue;
                }
            }

            // Similitudes
            if (criterioSeleccionado == "titulo") {
                const porcentajeSimilitud = calcularSimilitud(busquedaNormalizada,tituloNormalizado);
                if (porcentajeSimilitud > 0.7) {
                    res.similitud = porcentajeSimilitud
                    resultadosBusqueda.Similitudes.push(res)
                    continue;
                }
                
            } else {
                const porcentajeSimilitud = calcularSimilitud(busquedaNormalizada,tituloOriginalNormalizado);
                if (porcentajeSimilitud > 0.7) {
                    res.similitud = porcentajeSimilitud
                    resultadosBusqueda.Similitudes.push(res)
                    continue;
                }
            }
        }
        // Si hay coincidencias omitir las similitudes
        if (resultadosBusqueda.Coincidencias.length > 0) {
            resultadosBusqueda.Similitudes = []
        }

        resultadosBusqueda.BusquedaRealizada = true

        resultadosBusqueda = resultadosBusqueda;
        realizandoBusqueda = false;
    }
</script>

{#if recognitionDisponible == false}
    <article>
        <h3>¡Atención!</h3>
        <p>
            Tu navegador no soporta el reconocimiento por voz, consulta la lista
            de navegadores que lo permitan en la web <a
                href="https://caniuse.com/?search=SpeechRecognition"
                target="_blank">Can I use?</a
            >. En este caso, te recomendamos utilizar algún navegador de la
            familia de Chromium.
        </p>
    </article>
{/if}

<form on:submit|preventDefault={buscar}>
    {#if recognitionDisponible}
        <div id="contenedor-microfono">
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div id="microfono" on:click={reconocimientoVoz}>
                <svg
                    version="1.0"
                    id="Layer_1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                    width="64px"
                    height="64px"
                    viewBox="0 0 64 64"
                    enable-background="new 0 0 64 64"
                    xml:space="preserve"
                    fill="#fff"
                    ><g id="SVGRepo_bgCarrier" stroke-width="0" /><g
                        id="SVGRepo_tracerCarrier"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    /><g id="SVGRepo_iconCarrier">
                        <g>
                            <path
                                fill="#fff"
                                d="M32,48c7.732,0,14-6.268,14-14v-3h-7c-0.553,0-1-0.447-1-1s0.447-1,1-1h7v-4h-7c-0.553,0-1-0.447-1-1 s0.447-1,1-1h7v-4h-7c-0.553,0-1-0.447-1-1s0.447-1,1-1h7v-3c0-7.732-6.268-14-14-14S18,6.268,18,14v3h7c0.553,0,1,0.447,1,1 s-0.447,1-1,1h-7v4h7c0.553,0,1,0.447,1,1s-0.447,1-1,1h-7v4h7c0.553,0,1,0.447,1,1s-0.447,1-1,1h-7v3C18,41.732,24.268,48,32,48z"
                            />
                            <path
                                fill="#fff"
                                d="M51,31.002c-1.657,0-2.999,1.343-3,3C47.999,42.838,40.837,50,32,50s-15.999-7.162-16-15.998 c0-1.657-1.343-3-3-3s-3,1.343-3,3c0,10.429,7.26,19.156,17,21.422V60c0,2.209,1.791,4,4,4h2c2.209,0,4-1.791,4-4v-4.576 c9.74-2.266,17-10.993,17-21.422C53.999,32.345,52.657,31.002,51,31.002z M37,53.346c-0.654,0.168-1.321,0.304-2,0.406v1.247v0.794 V60c0,1.104-0.896,2-2,2h-2c-1.104,0-2-0.896-2-2v-4.207v-0.794v-1.247c-0.679-0.103-1.346-0.238-2-0.406 c-8.621-2.224-15-10.029-15-19.344c0-0.554,0.447-1,1-1s1,0.446,1,1C14.001,43.941,22.059,52,32,52s17.999-8.059,18-17.998 c0.001-0.552,0.447-1,1-1s0.999,0.448,1,1C52,43.316,45.621,51.122,37,53.346z"
                            />
                        </g>
                    </g></svg
                >
            </div>
        </div>
    {/if}
    <input id="busqueda" type="text" bind:value={busqueda} required />
    <label for="criterio-busqueda">Criterio búsqueda:</label>
    <select id="criterio-busqueda" bind:value={criterioSeleccionado} required>
        {#each criteriosBusqueda as busqueda}
            <option value={busqueda.valor}>{busqueda.texto}</option>
        {/each}
    </select>
    <fieldset>
        <legend>Idioma búsqueda:</legend>
        <label for="es">
            <input
                type="radio"
                id="es"
                bind:group={idioma}
                name="idioma"
                value="es-ES"
                checked
            />
            Español
        </label>
        <label for="en">
            <input
                type="radio"
                id="en"
                bind:group={idioma}
                name="idioma"
                value="en-EN"
            />
            Inglés
        </label>
    </fieldset>
    <button aria-busy={realizandoBusqueda}>Buscar</button>
</form>

<style>
    #contenedor-microfono {
        text-align: center;
    }
    #microfono {
        display: inline-block;
        padding: 5px;
        border-radius: 100%;
        background: #1095c1;
        margin: 20px auto 20px auto;
        cursor: pointer;
    }
</style>
