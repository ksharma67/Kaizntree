import { createRouter, createWebHistory } from 'vue-router'
import AppView from '../views/AppView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: AppView
  },
  {
    path: '/dasboard',
    name: 'dashboard',
    component: () => import(/* webpackChunkName: "about" */ '../views/UserDashboard.vue')
  },
  {
    path: '/items',
    name: 'Item Dashboard',
    component: () => import(/* webpackChunkName: "about" */ '../views/ItemDasboard.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
