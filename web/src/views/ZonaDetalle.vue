<template>
  <div class="mouseover">
    <span @mouseover="changeShow"><a v-bind:href="'/zona_inundable/'+zone.id"> {{ zone.nombre }} </a></span>
    <span v-show="active"> - Color: {{ zone.color }}</span>
    <span v-show="active"> - Código: {{ zone.codigo }}</span>
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