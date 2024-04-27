import { createRouter, createWebHistory } from 'vue-router'
import AppView from '../views/AppView.vue'

// Define the routes
const routes = [
  {
    path: '/',
    name: 'home',
    component: AppView
  },
  {
    path: '/dasboard',
    name: 'dashboard',
    // Use dynamic import to load the component lazily
    component: () => import(/* webpackChunkName: "about" */ '../views/UserDashboard.vue')
  },
  {
    path: '/items',
    name: 'Item Dashboard',
    // Use dynamic import to load the component lazily
    component: () => import(/* webpackChunkName: "about" */ '../views/ItemDasboard.vue')
  }
]

// Create the router instance
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Use the HTML5 history mode
  routes // Pass the defined routes
})

export default router
