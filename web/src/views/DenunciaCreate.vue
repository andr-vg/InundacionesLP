<template>
  <div>
    <l-map style="height: 450px" :zoom="zoom" :center="center" @click="onClick">
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="markerLatLng"></l-marker>
    </l-map>
  </div>
  <div>
    <li v-if="success">{{ success }}</li>
    <li v-for="(error, index) in errors" :key="index">{{ error }}</li>
    <label for="">Título</label>
    <input placeholder="Título" v-model="title" />
    <select v-model="category">
      <option disabled value="">Seleccione una categoria</option>
      <option
        v-for="(categoria, index) in categories"
        :key="index"
        v-bind:value="categoria.id"
      >
        {{ categoria.name }}
      </option>
    </select>
    <label for="">Descripcion</label>
    <textarea
      row="3"
      placeholder="Descripción"
      v-model="description"
    ></textarea>
    <label for="">Teléfono</label>
    <input placeholder="Teléfono" v-model="tel" />
    <label for="">Email</label>
    <input placeholder="Email" v-model="email" />
    <label for="">Nombre</label>
    <input placeholder="Nombre" v-model="firstname" />
    <label for="">Apellido</label>
    <input placeholder="Apellido" v-model="lastname" />
    <button @click="save">Guardar</button>
  </div>
</template>
<script>
import axios from "axios";
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

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
      description: "",
      tel: "",
      email: "",
      firstname: "",
      lastname: "",
      errors: [],
      success: "",
    };
  },
  methods: {
    save() {
      this.checkForm();
      if (this.errors.length == 0) {
        axios
          .post(
            "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/denuncias/",
            {
              title: this.title,
              category: this.category,
              description: this.description,
              lat: this.markerLatLng.lat,
              long: this.markerLatLng.lng,
              firstname: this.firstname,
              lastname: this.lastname,
              tel: this.tel,
              email: this.email,
            }
          )
          .then((response) => {
            console.log(response.status);
            if (response.status == 201) {
              this.success = "Denuncia cargada exitosamente";
            }
          })
          .catch((error) => {
            if (error.response) {
              this.errors.push(error.response.data.error_description);
            }
          });
      }
    },
    onClick(e) {
      if (e.latlng) {
        this.markerLatLng = e.latlng;
      }
    },

    get_categoria() {
      return axios
        .get("http://127.0.0.1:5000/api/categorias/")
        .then((response) => {
          // JSON responses are automatically parsed.
          this.categories = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
    validEmail(email) {
      let re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
    validTel(tel) {
      let re = /^(\(?\+[\d]{1,3}\)?)\s?([\d]{1,5})\s?([\d][\s.-]?){6,7}$/;
      return re.test(tel);
    },
    validName(name) {
      let re = /^[a-zA-Z]+$/;
      return re.test(name);
    },
    checkForm() {
      this.errors = [];
      this.success = "";
      if (!(this.category in this.categories)) {
        this.errors.push("Seleccione una categoria valida");
      }
      if (!this.validEmail(this.email)) {
        this.errors.push("Email invalido");
      }
      if (!this.validTel(this.tel)) {
        this.errors.push("Teléfono invalido");
      }
      if (!this.validName(this.firstname)) {
        this.errors.push("Nombre invalido");
      }
      if (!this.validName(this.lastname)) {
        this.errors.push("Apellido invalido");
      }
      if (this.description.length == 0 && this.description != " ") {
        this.errors.push("Debe ingresar una descripción");
      }
      if (this.title.length == 0 && this.title != " ") {
        this.errors.push("Debe ingresar un titulo");
      }
      if (this.markerLatLng.length == 0) {
        this.errors.push("Debe seleccionar un punto en el mapa");
      }
      if (this.markerLatLng.lat > 90 || this.markerLatLng.lat < -90) {
        this.errors.push("Debe ingresar una latitud válida");
      }
      if (this.markerLatLng.lng > 180 || this.markerLatLng.lng < -180) {
        this.errors.push("Debe ingresar una longitud válida");
      }
    },
  },
  created() {
    this.get_categoria();
  },
};
</script>
