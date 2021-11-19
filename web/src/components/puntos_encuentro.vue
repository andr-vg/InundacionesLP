<template>
 <div>
 <h1>Puntos de encuentro:</h1>
 <ul v-if="puntos && puntos.length">
 <li v-for="(punto, index) in puntos"
:key="index">
 {{ punto.name }}
 </li>
 </ul>
 <ul v-if="errors && errors.length">
 <li v-for="(error, index) in errors" :key="index">
 {{error.message}}
 </li>
 </ul>
 </div>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            puntos: [],
            errors: []
        }
    },
 // Fetches posts when the component is created.
 created() {

axios.get('http://127.0.0.1:5000/api/puntos_encuentro/')
 .then(response => {
 // JSON responses are automatically parsed.
    this.puntos = response.data;
 })
 .catch(e => {
    this.errors.push(e)
 })
 }
}
</script>