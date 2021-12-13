<template>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

  <link rel="stylesheet" type="text/css" :href="customerStyle" />
  <header>
     <fixed-header>
    <div class="navbar">
    
	<logo>
      <img class="logo" src="./assets/logo.png" alt="InundacionesLP">
  </logo>

  <div class="active">    
    <label for="check" id="checkbtn" class="checkbtn">
      <i class="fas fa-bars"></i>
    </label>
  </div>
  
  
	<menu_bar>
    <input type="checkbox" id="check" class="active">
		<line_menu>
      <menu><router-link to="/home">Home</router-link></menu>
			<menu><router-link :to="{name:'zonas_inundables', params: {page: 1}}">Zonas inundables</router-link></menu>
			<menu><router-link to="/puntos_y_recorridos">Puntos y recorridos </router-link></menu>
			<menu><router-link :to="{ name: 'denuncia', params: { page: 1 } }">Denuncias</router-link></menu>
		</line_menu>
	</menu_bar>
  
  <div id="app">
    <div class="nav" id="nav">
  </div>

  
  </div>

  </div>
  </fixed-header>
</header>
  
  <router-view />

</template>
<script>
import axios from "axios";
import FixedHeader from 'vue-fixed-header'
export default {
  components: {
    FixedHeader
  },
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
.navbar.vue-fixed-header--isFixed {
  position: fixed;
  left: 0;
  top: 0;
  width: 100vw;
}

</style>



