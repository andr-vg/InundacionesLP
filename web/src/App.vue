<template>

  <link rel="stylesheet" type="text/css" :href="customerStyle" />
  <div id="app">
    <div class="nav" id="nav">
      <router-link to="/home">Home</router-link>
      <router-link :to="{name:'zonas_inundables', params: {page: 1}}">Zonas inundables</router-link>
      <router-link to="/puntos_y_recorridos">Puntos y recorridos </router-link>
      <router-link to="/denuncia">Denuncias</router-link>
    </div>
  </div>
  <router-view />
</template>
<script>
import axios from "axios";
export default {
  data() {
    return {
      config: "",
    };
  },
  methods: {
    async get_configuration() {
      return axios
        .get(
          "http://127.0.0.1:5000/api/configuracion"
        )
        .then((response) => {
          this.config = response.data.css_public;
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  computed: {
    customerStyle() {
      this.get_configuration();
      return `${this.config}`;
    },
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
