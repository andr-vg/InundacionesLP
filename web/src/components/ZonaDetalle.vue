<template>
  <div class="mouseover">
    <div @mouseover="changeShow">Zona: {{ zone.nombre }}</div>
    <div v-show="active">Color: {{ zone.color }}</div>
  </div>
</template>
<script>
export default {
  el: ".mouseover",
  props: {
    zone: Object,
  },
  data() {
    return {
      active: false,
    };
  },
  methods: {
    changeShow() {
      this.active = !this.active;
    },
  },
};
</script>