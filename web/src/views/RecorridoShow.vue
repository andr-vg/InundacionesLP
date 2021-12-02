<template>
  <div @click="changeShow">
    <div v-if="show" class="box">
      <p>{{ recorrido.nombre }}</p>
      <p>Descripcion:{{ recorrido.descripcion }}</p>
    </div>
    <div v-else>
      <p>{{ recorrido.nombre }}</p>
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
