<template>
  <div>
    <h1>Zonas inundables</h1>
    <div>
      <l-map style="height: 450px" :zoom="zoom" :center="center">
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <div v-for="(zone, index) in zones" :key="index">
          <l-polygon
            :lat-lngs="zone.coordenadas.map(({ lat, long }) => [lat, long])"
            :color="zone.color"
            :fill="true"
            :fillColor="zone.color"
            :fillOpacity="0.3"
          >
            <l-popup>{{ zone.nombre }} </l-popup>
          </l-polygon>
        </div>
      </l-map>
      <div class="container">
        <h2>Información</h2>
        <ul v-if="zones && zones.length">
          <li v-for="(zone, index) in zones" :key="index">
            <detalleZone :zone="zone"></detalleZone>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { LMap, LTileLayer, LPolygon, LPopup } from "@vue-leaflet/vue-leaflet";
import detalleZone from "./ZonaDetalle.vue";

export default {
  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LPopup,
    detalleZone,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [-34.90397977693234, -57.947371498538885],
      zoom: 11.5,
      zones: [],
      showZone: false,
    };
  },
  // consultamos a la api ni bien se crea la componente
  created() {
    // y en caso de exito jsonificamos la respuesta de la api
    fetch("http://localhost:5000/api/zonas_inundables")
      .then((response) => {
        console.log(response);
        return response.json();
      })
      .then((json) => {
        console.log(json);
        this.zones = json.zonas;
      })
      .catch((e) => {
        console.log(e);
      });
  },
};
</script>
