<template>  
  <div>
    <br>
    <h1>Zonas inundables</h1>
    <div>
      <div class="flex">
        <Map>
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
        </Map>
      <br>
      <div class="elem">
        <h2>Información</h2>
        <div >
          <ul v-if="zones && zones.length">
          <li v-for="(zone, index) in zones" :key="index" >
            <detalleZone class="container" style="width: fit-content" :zone="zone"></detalleZone>
          </li>
        </ul>
        </div>
        
      </div>
      </div>
<Paginado :previousPage=previousPage  :nextPage=nextPage :pagina=pagina :index=index />
         
    </div>

  </div>

</template>


<script>
import axios from "axios";
import {LPolygon, LPopup } from "@vue-leaflet/vue-leaflet";
import detalleZone from "./ZonaDetalle.vue";
import Map from './../components/Map.vue'
import Paginado from './../components/Paginado.vue';

export default {
  components: {
    Map,
    LPolygon,
    LPopup,
    detalleZone,
    Paginado,   
    
  },
  data() {
    return {
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




