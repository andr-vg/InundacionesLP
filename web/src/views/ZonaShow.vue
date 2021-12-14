<template>
  <div>
      <h1>Detalle</h1>
      <div>
          <l-map id="map" style="height: 450px; width: 90%; margin:auto" :zoom="zoom" :center="[parseFloat(this.zone.coordenadas[1].lat), parseFloat(this.zone.coordenadas[1].long)]" @update:center="forceRenderer">
          <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
          <div>
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
      </div>
      <br>
              <h2>Información</h2>

      <div class="box item3" style="padding:0%; width: fit-content; margin: auto; background-color: lightblue">
        <div>Zona: {{ zone.nombre }}</div>
        <div>Color: {{ zone.color }}</div>
        <div>Código: {{ zone.codigo }}</div>
      </div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import { LMap, LTileLayer, LPolygon, LPopup } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LPolygon,
    LPopup,
  },

  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      center: [-34.90397977693234, -57.947371498538885],
      zoom: 12,
      zone: [],
    };
  },
  
  // consultamos a la api ni bien se crea la componente
  methods: {
      forceRenderer(){
        this.center = Object.values([parseFloat(this.zone.coordenadas[1].lat), parseFloat(this.zone.coordenadas[1].long)]);
      }
  },
  created() {
        fetch("https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/zonas_inundables/"+document.location.pathname.split('/').at(-1))
            .then((response) => {
                return response.json();
            })
            .then((json) => { 
                this.zone = json.atributos; 
                this.forceRenderer();
            }).catch((e) => {
                console.log(e);
            })
            
            
  },
  
}
</script>

