<template>
  <div>
    <div v-if="show" class="box">
      <p>{{ recorrido.nombre }}</p>
      <p>Descripcion:{{ recorrido.descripcion }}</p>
      <p @click="changeShow">Mostrar menos</p>
    </div>
    <div v-else @click="changeShow">
      <span>Mostrar mas</span>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    recorrido: Object,
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
