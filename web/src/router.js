import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/HelloWorld.vue'
import PuntosYRecorridos from './components/PuntosYRecorridos.vue'
import Denuncias from './components/DenunciaCreate.vue'
import ZonasInundables from './components/ZonasInundables.vue'

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
        path: '/denuncia',
        name: 'denuncia',
        component: Denuncias
    },
    {
        path: '/zonas_inundables',
        name: 'zonas_inundables',
        component: ZonasInundables
    },

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router