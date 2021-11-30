<template>
  <div @click="changeShow">
    <div v-if="show">
      {{ recorrido.nombre }}
      {{ recorrido.descripcion }}
    </div>
    <div v-else>
      {{ recorrido.nombre }}
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
