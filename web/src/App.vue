<template>
  <link rel="stylesheet" type="text/css" :href="customerStyle" />
  <header>
	<logo>
      <img class="logo" src="./assets/logo.png" alt="InundacionesLP">
  </logo>
  
	<menu_bar>
		<line_menu>
      <menu><router-link to="/home">Homes</router-link></menu>
			<menu><router-link :to="{name:'zonas_inundables', params: {page: 1}}">Zonas inundables</router-link></menu>
			<menu><router-link to="/puntos_y_recorridos">Puntos y recorridos </router-link></menu>
			<menu><router-link :to="{ name: 'denuncia', params: { page: 1 } }">Denuncias</router-link></menu>
		</line_menu>
	</menu_bar>
  <div id="app">
    <div class="nav" id="nav">
  </div>
  </div>
</header>
  
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
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/configuracion"
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



