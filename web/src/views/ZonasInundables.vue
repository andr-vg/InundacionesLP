<template>
  
  <div>

    <br>
    <h1>Zonas inundables</h1>
    <div>
      <div class="flex">
      <l-map style="height: 450px; width: 90%; margin:auto" :zoom="zoom" :center="center" class="elem">
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
      <div class="elem">
        <h2>Información</h2>
        <ul v-if="zones && zones.length">
          <li v-for="(zone, index) in zones" :key="index">
            <detalleZone :zone="zone"></detalleZone>
          </li>
        </ul>
      </div>
      </div>

      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li v-if="previousPage != null" class="page-item"><a class="page-link" v-bind:href="previousPage">Anterior</a></li>
          <li v-for="(pagina, index) in total" :key="index" class="page-item" v-bind:class="isActive(pagina)"><a class="page-link" v-bind:href="pagina">{{ pagina }}</a></li>
          <li v-if="nextPage != null" class="page-item"><a class="page-link" v-bind:href="nextPage">Siguiente</a></li>
        </ul>

      </nav>     
    </div>

  </div>

</template>


<script>
import axios from "axios";

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
      center: [-34.898575851767255, -57.95788336826374],
      zoom: 11,
      zones: [],
      showZone: false,
      actualPage: document.location.pathname.split('/').at(-1),
      previousPage: null,
      nextPage: null,
      total: 1,
      baseUrl: window.location.href,
    };
  },
  methods : {
    get_zonas() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/zonas_inundables/?page="+document.location.pathname.split('/').at(-1),
        )
        .then((response) => {
          // JSON responses are automatically parsed.
          this.zones = response.data.zonas;
          const totalRows = response.data.total;
          const per_page = response.data.por_pagina;
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
        return 'active';
      } else {
        return '';
      }
    },
    
  },
  // consultamos a la api ni bien se crea la componente
  created() {
    this.get_zonas();
  },
 
 
};
</script>

<style>

  a, a:hover {
    color: rgb(255, 255, 255);
  }

  .elem {
  width: 50%;
  }


  
</style>




