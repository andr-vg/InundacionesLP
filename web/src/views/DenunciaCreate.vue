<template>
  <h1>Carga tu denuncia</h1>
  <span class="success" v-if="success">{{ success }}</span>
  <ul>
    <li class="errors" v-for="(error, index) in errors" :key="index">
      {{ error }}
    </li>
  </ul>
  <div class="container">
    <div class="item4">
      <l-map
        style="height: 450px"
        :zoom="zoom"
        :center="center"
        @click="onClick"
      >
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-marker
          v-if="markerLatLng.length != 0"
          :lat-lng="markerLatLng"
        ></l-marker>
      </l-map>
    </div>
    <div class="item5">
      <div class="container">
        <div class="item3">
          <label for="">Título*</label>
          <input placeholder="Título" v-model="title" />
        </div>
        <div class="item3">
          <label for="">Categoría</label>
          <select v-model="category">
            <option disabled value="">Seleccione una categoria*</option>
            <option
              v-for="(categoria, index) in categories"
              :key="index"
              v-bind:value="categoria.id"
            >
              {{ categoria.name }}
            </option>
          </select>
        </div>
        <div class="item3">
          <label for="">Descripción*</label>
          <textarea
            row="3"
            placeholder="Descripción"
            v-model="description"
          ></textarea>
        </div>
        <div class="item3">
          <label for="">Teléfono*</label>
          <input placeholder="Teléfono" v-model="tel" />
          <small id="telHelp" style="display: flex"
            >Ejemplo: +54 221 4567890</small
          >
        </div>
        <div class="item3">
          <label for="">Email*</label>
          <input placeholder="Email" v-model="email" />
          <small id="emailHelp" style="display: flex"
            >Ejemplo: InundacionesLP@mail.com</small
          >
        </div>
        <div class="item3">
          <label for="">Nombre*</label>
          <input placeholder="Nombre" v-model="firstname" />
        </div>
        <div class="item3">
          <label for="">Apellido*</label>
          <input placeholder="Apellido" v-model="lastname" />
        </div>
        <small class="item3" style="display: flex">* Campos obligatorios</small>
        <small class="item3" style="display: flex"
          >Se debe marcar un punto en el mapa</small
        >
        <button @click="save" class="item3">Guardar</button>
      </div>
    </div>
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

    async get_categoria() {
      return axios
        .get(
          "https://admin-grupo22.proyecto2021.linti.unlp.edu.ar/api/categorias/"
        )
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
      let categories = [];
      this.categories.forEach(function (value) {
        categories.push(value.id);
      });
      if (!categories.includes(this.category)) {
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
