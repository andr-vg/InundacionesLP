<template>
<div>
 <link rel="stylesheet" type="text/css"  href="../assets/style.css" /> 
<nav aria-label="Page navigation example">
    <ul class="pagination">
      <li v-if="previousPage != null" class="page-item"><a class="page-link" v-bind:href="previousPage">Anterior</a></li>
      <li v-for="(pagina, index) in total" :key="index" class="page-item" v-bind:class="isActive(pagina)"><a class="page-link" v-bind:href="pagina">{{ pagina }}</a></li>
      <li v-if="nextPage != null" class="page-item"><a class="page-link" v-bind:href="nextPage">Sig</a></li>
    </ul>

  </nav>
</div>
</template>
<script>

export default {
  name: 'Paginado',
  props: {
    previousPage:Object,
    nextPage:Object,
    pagina:Object,
    index:Object,
    total:Object,
  },
  methods: {
    isActive(nroPagina) {
      if (nroPagina == this.pagina) {
        return 'active';
      } else {
        return '';
      }
    },

  },
}
</script>


