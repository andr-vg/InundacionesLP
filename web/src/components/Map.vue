<template>
  <div>
    <l-map style="height: 450px; width: 90%; margin:auto" :zoom="zoom" :center="center">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <slot></slot>
    </l-map>
  </div>
</template>
<script>


import { LMap, LTileLayer} from "@vue-leaflet/vue-leaflet";
export default {
  name: "Map",
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