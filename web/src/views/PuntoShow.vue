<template>
  <div @click="changeShow">
    <div v-if="show" class="box">
      <p>{{ punto.name }}</p>
      <p>Descripción: {{ punto.description }}</p>
      <p>Dirección: {{ punto.address }}</p>
      <p>Teléfono: {{ punto.tel }}</p>
      <p>Email: {{ punto.email }}</p>
    </div>
    <div v-else>
      <p>{{ punto.name }}</p>
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
