<template>
  <div>
    <l-map style="height: 450px" :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(punto, index) in puntos" :key="index">
        <l-marker :lat-lng="punto.coords.split(',')"></l-marker>
      </div>
    </l-map>
  </div>
  <div class="PuntosYRecorridos">
    <h1>Puntos de encuentro:</h1>
    <ul v-if="puntos && puntos.length">
      <li v-for="(punto, index) in puntos" :key="index">
        {{ punto.name }}
      </li>
    </ul>
    <ul v-if="errors && errors.length">
      <li v-for="(error, index) in errors" :key="index">
        {{ error.message }}
      </li>
    </ul>
  </div>
</template>
<script>
import axios from "axios";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [-34.9187, -57.956],
      puntos: [],
      errors: [],
    };
  },
  // Fetches posts when the component is created.
  created() {
    axios
      .get("http://127.0.0.1:5000/api/puntos_encuentro/")
      .then((response) => {
        // JSON responses are automatically parsed.
        this.puntos = response.data;
      })
      .catch((e) => {
        this.errors.push(e);
      });
  },
};
</script>
