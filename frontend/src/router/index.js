import { createWebHistory, createRouter } from 'vue-router'

import Catalog from '../pages/Catalog.vue'
import CategoryPage from '../pages/CategoryPage.vue'
import ProductDetail from '../pages/ProductDetail.vue'
import LoginPage from '../pages/LoginPage.vue'
import SignupPage from '../pages/SignupPage.vue'

const routes = [
  { path: '/products', component: Catalog },
  { path: '/categories/:slug', component: CategoryPage, name: 'category' },
  { path: '/products/:id', component: ProductDetail, name: 'product-detail' },
  { path: '/login', component: LoginPage, name: 'login' },
  { path: '/signup', component: SignupPage, name: 'signup' },
]

export const router = createRouter({
  history: createWebHistory(), // update url depending on the path
  routes,
})

export default router
