import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/HelloWorld.vue'
import PuntosYRecorridos from './components/PuntosYRecorridos.vue'

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

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router