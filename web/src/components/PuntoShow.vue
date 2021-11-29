<template>
  <div @click="changeShow">
    <div v-if="show">
      {{ punto.description }}
      {{ punto.name }}
      {{ punto.address }}
      {{ punto.tel }}
      {{ punto.email }}
    </div>
    <div v-else>
      {{ punto.name }}
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
