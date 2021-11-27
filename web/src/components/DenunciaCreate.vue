<template>
  <div>
    <l-map style="height: 450px" :zoom="zoom" :center="center" @click="onClick">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="markerLatLng"></l-marker>
    </l-map>
  </div>
  <div>
    <label for="">Título</label>
    <input placeholder="Título" v-model="title">
    <select v-model="category" >
    <option disabled value="">Seleccione una categoria</option>
    <option v-for="(categoria,index) in categories" :key="index" v-bind:value="categoria.id">{{ categoria.name }}</option>
    </select>
    <label for="">Descripcion</label>
    <textarea row="3" placeholder="Descripción" v-model="description"></textarea>
    <label for="">Teléfono</label>
    <input placeholder="Teléfono" v-model="tel">
    <label for="">Email</label>
    <input placeholder="Email" v-model="email">
    <label for="">Nombre</label>
    <input placeholder="Nombre" v-model="firstname">
    <label for="">Apellido</label>
    <input placeholder="Apellido" v-model="lastname">
    <button @click="save">Guardar</button>
    <p>{{ markerLatLng }}</p>
  </div>
</template>
<script>
import axios from "axios";
import {
  LMap,
  LTileLayer,
  LMarker,
} from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      attribution:
        '&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      zoom: 15,
      center: [-34.9187, -57.956],
      categories: [],
      markerLatLng: [],
      title: "",
      category: "",
      description:"",
      tel:"",
      email:"",
      firstname:"",
      lastname:"",
    };
  },
    methods: {
        save(){
            axios.post('http://127.0.0.1:5000/api/denuncias/', {
                title:this.title,
                category:this.category,
                description:this.description,
                lat:this.markerLatLng.lat,
                long:this.markerLatLng.lng,
                firstname:this.firstname,
                lastname:this.lastname,
                tel:this.tel,
                email:this.email}
            ).catch(function (error) {
                console.log(error);
            });

        },
        onClick(e){
            if(e.latlng){
                this.markerLatLng = e.latlng;
            }
        },

        get_categoria() {
            return axios.get("http://127.0.0.1:5000/api/categorias/")
            .then((response) => {
            // JSON responses are automatically parsed.
            this.categories = response.data;
            })
            .catch((e) => {
            this.errors.push(e);
            });
    },
    },
    created(){
        this.get_categoria()
    },
}
</script>