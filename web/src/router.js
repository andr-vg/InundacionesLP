import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import PuntosYRecorridos from './views/PuntosYRecorridos.vue'
import Denuncias from './views/Denuncias.vue'
import DenunciaCreate from './views/DenunciaCreate.vue'
import ZonasInundables from './views/ZonasInundables.vue'
import ZonaInundableShow from './views/ZonaShow.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/puntos_y_recorridos',
        name: 'puntos_y_recorridos',
        component: PuntosYRecorridos
    },
    {
        path: '/denuncia/:page',
        name: 'denuncia',
        component: Denuncias
    },
    {
        path: '/denuncia/nueva',
        name: 'denunciacrear',
        component: DenunciaCreate
    },
    {
        path: '/zonas_inundables/:page',
        name: 'zonas_inundables',
        component: ZonasInundables,
        
    },
    {
        path: '/zona_inundable/:id',
        name: 'zona_inundable',
        component: ZonaInundableShow
    },

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router