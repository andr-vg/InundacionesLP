<template>
  <div>
    <br>
    <h1>Denuncias</h1>
    <br>
    <a class="page-link" style="width: fit-content; margin: auto;" v-bind:href="'/denuncia/nueva'"> Crear denuncia</a>
    <br>
    <l-map style="height: 450px; width: 90%; margin:auto" :zoom="zoom" :center="center">
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
    };
  },
  methods: {
    async get_denuncias() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/denuncias/"
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          this.denuncias = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
  },
  // Fetches posts when the component is created.
  created() {
    this.get_denuncias();
  },
};
</script>
