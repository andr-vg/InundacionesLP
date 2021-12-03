<template>
  <div>
    <div v-if="show" class="box">
      <p>Descripción: {{ punto.description }}</p>
      <p>Dirección: {{ punto.address }}</p>
      <p>Teléfono: {{ punto.tel }}</p>
      <p>Email: {{ punto.email }}</p>
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
    punto: Object,
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
