<template>
  <span class="item1">{{ punto.name }}</span>
  <span v-if="show" @click="changeShow" class="item2">Mostrar menos</span>
  <span v-else @click="changeShow" class="item2">Mostrar mas</span>
  <div v-if="show" class="box item3">
    <p>Descripción: {{ punto.description }}</p>
    <p>Dirección: {{ punto.address }}</p>
    <p>Teléfono: {{ punto.tel }}</p>
    <p>Email: {{ punto.email }}</p>
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
