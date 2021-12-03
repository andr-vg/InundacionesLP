<template>
<!--<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
-->
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
      <nav aria-label="Page navigation example">
        <ul class="pagination">
          <li v-if="previousPage != null" class="page-item"><a class="page-link" v-bind:href="previousPage">Anterior</a></li>
          <li v-for="(pagina, index) in total" :key="index" class="page-item" v-bind:class="isActive(pagina)"><a class="page-link" v-bind:href="pagina">{{ pagina }}</a></li>
          <li v-if="nextPage != null" class="page-item"><a class="page-link" v-bind:href="nextPage">Siguiente</a></li>
        </ul>

      </nav>     
    </div>
  </div>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

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
      center: [-34.90397977693234, -57.947371498538885],
      zoom: 11.5,
      zones: [],
      showZone: false,
      actualPage: this.$route.params.page,
      previousPage: null,
      nextPage: null,
      total: 1,
      baseUrl: window.location.href,
    };
  },
  /*
  mounted() {
    this.actualPage = 1;
  },
  */
  methods : {
    get_zonas() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/zonas_inundables/?page="+this.$route.params.page,
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
    /*
    getActualPage(){
      if (!this.$route.params.page){
        console.log("entre aca");
        return 1;
      } else {
        return this.$route.params.page;
      }
    }
    */
  },
  // consultamos a la api ni bien se crea la componente
  created() {
    this.get_zonas();
  },
  /*
  updated() {
    //this.setTotalPages();
    //console.log(this.total);
    //this.actualPage = this.actualPage + 1;
    //this.get_zonas();
  }
  */
};

</script>

