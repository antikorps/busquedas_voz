<script lang="ts">
    import Advertencia from "./lib/Advertencia.svelte";
import Buscador from "./lib/Buscador.svelte";
    import Resultados from "./lib/Resultados.svelte";
    import type { ResultadosBusqueda } from "./modelos";

    let resultadosBusqueda: ResultadosBusqueda = {
        BusquedaRealizada: false,
        Coincidencias: [],
        Similitudes: [],
    };

</script>

<main class="container">
  <Advertencia></Advertencia>
  <Buscador bind:resultadosBusqueda></Buscador>
  <Resultados bind:resultadosBusqueda></Resultados>
</main>

<style>
  main {
    margin-top: 30px;
  }
</style>