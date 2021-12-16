


<template>
  
  <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css"
    rel="stylesheet"
    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC"
    crossorigin="anonymous"
  />

  <link rel="stylesheet" type="text/css" :href="customerStyle" />

  <header>
        <div class="title">
            <div class="logo">
                <router-link to="/home">
                    <img class="logo" src="./assets/logo.png" alt="InundacionesLP" />
                </router-link>
            </div>
            <div class="title-page">
                <h1>InundacionesLP  </h1>
            </div>
            <div class="active">    
                <label for="check" id="checkbtn" class="checkbtn" @click="bringToFront">
                  <img src="./assets/bars-solid.svg" alt="Boton menu" />
                </label>
            </div>
        </div>
        <nav>
            <input type="checkbox" id="check" class="active">
            <ul>
                <li><router-link @click="close" to="/home">HOME</router-link></li>
                <li><router-link @click="close" :to="{ name: 'zonas_inundables', params: { page: 1 } }"
            >ZONAS INUNDABLES</router-link
          ></li>
                <li><router-link @click="close" to="/puntos_y_recorridos"
            >PUNTOS Y RECORRIDOS
          </router-link></li>
                <li><router-link @click="close" :to="{ name: 'denuncia', params: { page: 1 } }"
            >DENUNCIAS</router-link
          ></li>
            </ul>
        </nav>
    </header>
  <br>
  <!--
  <header>
    <logo>
      <img class="logo" src="./assets/logo.png" alt="InundacionesLP" />
    </logo>

    <div class="active">
      <label for="check" id="checkbtn" class="checkbtn">
        <i class="fas fa-bars"></i>
      </label>
    </div>

    <menu_bar>
      <input type="checkbox" id="check" class="active" />
      <line_menu>
        <menu><router-link to="/home">Home</router-link></menu>
        <menu
          ><router-link :to="{ name: 'zonas_inundables', params: { page: 1 } }"
            >Zonas inundables</router-link
          ></menu
        >
        <menu
          ><router-link to="/puntos_y_recorridos"
            >Puntos y recorridos
          </router-link></menu
        >
        <menu
          ><router-link :to="{ name: 'denuncia', params: { page: 1 } }"
            >Denuncias</router-link
          ></menu
        >
      </line_menu>
    </menu_bar>

    <div id="app">
      <div class="nav" id="nav"></div>
    </div>
  </header>
  -->
 
  <router-view />
   <footer>
     <br>
     <br>
     <br>
     <br>
     <br>

  <div class="links">
        <a href="https://www.facebook.com/InundacionesLP" target="_blank"><i class="fab fa-facebook"></i></a>
        <a href="https://www.instagram.com/InundacionesLP" target="_blank"><i class="fab fa-instagram"></i></a>
        <a href="https://www.twitter.com/InundacionesLP" target="_blank"><i class="fab fa-twitter"></i></a>
    </div>
    <p> Copyright 2021 © Todos los derechos reservados.</p>
</footer>
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
    close() {
      document.getElementById("check").checked = false;
      this.bringToFront();
    },
    bringToFront() {
    
    var forms = document.getElementsByClassName("frontTo");
    var forms2 = document.getElementsByClassName("leaflet-container leaflet-touch leaflet-grab leaflet-touch-drag leaflet-touch-zoom");
    if (document.getElementById("checkbtn").style.zIndex == ""){
        document.getElementById("checkbtn").style.zIndex = 10;  
        for (let form of forms){
            form.style.zIndex = -1;
        }       
        for (let form of forms2){
            form.style.zIndex = -1;
        }
    } else {
        // bring to back
        document.getElementById("checkbtn").style.zIndex = "";
        for (let form of forms){
            form.style.zIndex = 0;
        }
        for (let form of forms2){
            form.style.zIndex = 0;
        }
    }
    
},
    async get_configuration() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/configuracion"
        )
        .then((response) => {
          this.config = "/" + response.data.css_public;
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
}

</script>
<style>




#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
