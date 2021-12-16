<template>
  <div class="frontTo">
    <l-map style="height: 450px; width: 90%; margin:auto" :zoom="zoomMap" :center="centerMap">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <slot></slot>
    </l-map>
  </div>
</template>
<script>


import { LMap, LTileLayer} from "@vue-leaflet/vue-leaflet";
export default {
  name: "Map",
  props: {
    zoomMap:Object,
    centerMap:Object,
  },
  components: {
    LMap,
    LTileLayer,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [-34.9187, -57.956],
    };
  },
};
</script>