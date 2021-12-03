<template>
  <div>
    <l-map
      style="height: 450px"
      :zoom="zoom"
      :center="center"
      @update:center="get_puntos"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(punto, index) in puntos" :key="index">
        <l-marker :lat-lng="punto.coords.split(',')">
          <l-popup
            >Nombre: {{ punto.name }} Correo: {{ punto.email }} Teléfono:
            {{ punto.tel }}
          </l-popup>
        </l-marker>
      </div>
      <div v-for="(recorrido, index) in recorridos" :key="index">
        <l-polyline
          :lat-lngs="recorrido.coordenadas"
          :color="color"
          :weight="2"
          @update:center="get_recorridos"
        >
          <l-popup>Nombre: {{ recorrido.nombre }}</l-popup>
        </l-polyline>
      </div>
    </l-map>
  </div>
  <div class="container">
    <div class="container-left">
      <h2>Puntos de encuentro</h2>
      <ul v-if="puntos && puntos.length">
        <li v-for="(punto, index) in puntos" :key="index">
          <span>{{ punto.name }}</span>
          <detallePunto :punto="punto"></detallePunto>
        </li>
      </ul>
      <ul v-if="errors && errors.length">
        <li v-for="(error, index) in errors" :key="index">
          {{ error.message }}
        </li>
      </ul>
    </div>
    <div class="container-right">
      <h2>Recorridos de evacuación</h2>
      <ul v-if="puntos && puntos.length">
        <li v-for="(recorrido, index) in recorridos" :key="index">
          <span>{{ recorrido.nombre }}</span>
          <detalleRecorrido :recorrido="recorrido"></detalleRecorrido>
        </li>
      </ul>
      <ul v-if="errors && errors.length">
        <li v-for="(error, index) in errors" :key="index">
          {{ error.message }}
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import {
  LMap,
  LTileLayer,
  LMarker,
  LPolyline,
  LPopup,
} from "@vue-leaflet/vue-leaflet";
import detallePunto from "./PuntoShow.vue";
import detalleRecorrido from "./RecorridoShow.vue";
export default {
  components: {
    LMap,
    LTileLayer,
    LPopup,
    LMarker,
    LPolyline,
    detallePunto,
    detalleRecorrido,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [-34.9187, -57.956],
      puntos: [],
      recorridos: [],
      color: "blue",
      errors: [],
      showPunto: false,
      showRecorrido: false,
    };
  },
  methods: {
    success_geolocation(position) {
      this.centerUpdated([position.coords.latitude, position.coords.longitude]);
    },
    async get_geolocation() {
      navigator.geolocation.getCurrentPosition(this.success_geolocation);
    },
    centerUpdated(center) {
      this.center = center;
    },
    async get_puntos() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/puntos_encuentro/cercanos",
          {
            params: {
              lat: this.center[0],
              lon: this.center[1],
            },
          }
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          this.puntos = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },

    get_recorridos() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/recorridos_evacuacion/cercanos",
          {
            params: {
              lat: this.center[0],
              lon: this.center[1],
            },
          }
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          this.recorridos = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
  },
  // Fetches posts when the component is created.
  created() {
    this.get_geolocation();
    this.get_puntos();
    this.get_recorridos();
  },
  updated() {
    this.get_geolocation();
  },
};
</script>
<style>
ul {
  list-style-type: none;
}
#container {
  margin: 200px;
  max-width: 48rem;
  width: 90%;
}
.container ul {
  text-align: left;
}
.container h2 {
  text-align: left;
}
</style>
