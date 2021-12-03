<template>
  <div>
    <a v-bind:href="'/denuncia/nueva'"> Crear denuncia</a>
    <l-map style="height: 450px" :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(denuncia, index) in denuncias" :key="index">
        <l-marker :lat-lng="denuncia.coordenadas.split(',')">
          <l-popup
            ><p>Datos del denunciante:</p>
            <p>Nombre:{{ denuncia.nombre_denunciante }}</p>
            <p>Apellido:{{ denuncia.apellido_denunciante }}</p>
            <p>Email:{{ denuncia.email_denunciante }}</p>
            <p>Teléfono:{{ denuncia.telcel_denunciante }}</p>
            <p>Estado:{{ denuncia.estado }}</p>
            <span>Descripción: {{ denuncia.descripcion }}</span>
          </l-popup>
        </l-marker>
      </div>
    </l-map>
    <nav aria-label="Page navigation example">
      <ul class="pagination">
        <li v-if="previousPage != null" class="page-item">
          <a class="page-link" v-bind:href="previousPage">Anterior</a>
        </li>
        <li
          v-for="(pagina, index) in total"
          :key="index"
          class="page-item"
          v-bind:class="isActive(pagina)"
        >
          <a class="page-link" v-bind:href="pagina">{{ pagina }}</a>
        </li>
        <li v-if="nextPage != null" class="page-item">
          <a class="page-link" v-bind:href="nextPage">Siguiente</a>
        </li>
      </ul>
    </nav>
  </div>
</template>
<script>
import axios from "axios";
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
export default {
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LMarker,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [-34.9187, -57.956],
      denuncias: [],
      actualPage: document.location.pathname.split("/").at(-1),
      previousPage: null,
      nextPage: null,
      total: 1,
      baseUrl: window.location.href,
    };
  },
  methods: {
    async get_denuncias() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/denuncias/?page=" +
            document.location.pathname.split("/").at(-1)
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          this.denuncias = response.data.denuncias;
          console.log(this.denuncias);
          const totalRows = response.data.total;
          const per_page = response.data.per_page;
          const resto = totalRows % per_page;
          this.total = parseInt(totalRows / per_page);
          if (resto != 0) {
            this.total = parseInt(this.total) + 1;
          }
          if (this.actualPage > 1) {
            this.previousPage = parseInt(this.actualPage) - 1;
          }
          if (this.actualPage < this.total) {
            this.nextPage = parseInt(this.actualPage) + 1;
          }
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    isActive(nroPagina) {
      if (nroPagina == this.actualPage) {
        return "active";
      } else {
        return "";
      }
    },
  },
  // Fetches posts when the component is created.
  created() {
    this.get_denuncias();
  },
};
</script>
