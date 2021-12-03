<template>
  <div class="mouseover">
    <span @mouseover="changeShow"><a v-bind:href="'/zonas_inundables/'+zone.id"> {{ zone.nombre }} </a></span>
    <span v-show="active"> - Color: {{ zone.color }}</span>
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