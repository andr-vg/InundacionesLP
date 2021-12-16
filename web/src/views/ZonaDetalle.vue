<template>
  <div>
    <span class="item1"><a v-bind:href="'/zona_inundable/'+zone.id"> {{ zone.nombre }} </a></span>
    <span v-if="show" @click="changeShow" class="item2 page-link" style="width: fit-content; margin: auto;">Mostrar menos</span>
    <span v-else @click="changeShow" class="item2 page-link" style="width: fit-content; margin: auto;">Mostrar mas</span>
    <div v-if="show" class="box item3">
      <p> Color: {{ zone.color_esp }}</p>
      <p> Código: {{ zone.codigo }}</p>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    zone: Object,
  },
  data() {
    return {
      show: false,
    };
  },
  methods: {
    changeShow() {
      this.show = !this.show;
    },
  },
};
</script>

