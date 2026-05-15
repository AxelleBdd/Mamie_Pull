import { createWebHistory, createRouter } from 'vue-router'

import Catalog from '../pages/Catalog.vue'
import CategoryPage from '../pages/CategoryPage.vue'
import ProductDetail from '../pages/ProductDetail.vue'
import LoginPage from '../pages/LoginPage.vue'
import SignupPage from '../pages/SignupPage.vue'
import HomePage from '../pages/HomePage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import AdminProducts from '../pages/AdminProducts.vue'
import AdminProductForm from '../pages/AdminProductForm.vue'
import { useAuthStore } from '../stores/authStore'

const routes = [
  { path: '/products', component: Catalog },
  { path: '/categories/:slug', component: CategoryPage, name: 'category' },
  { path: '/products/:id', component: ProductDetail, name: 'product-detail' },
  { path: '/login', component: LoginPage, name: 'login' },
  { path: '/register', component: SignupPage, name: 'signup' },
  { path: '/profile', component: ProfilePage, name: 'profile' },
  {
    path: '/admin/products',
    component: AdminProducts,
    name: 'admin-products',
    meta: { requiresStaff: true },
  },
  {
    path: '/admin/products/new',
    component: AdminProductForm,
    name: 'admin-product-new',
    meta: { requiresStaff: true },
  },
  {
    path: '/admin/products/:id/edit',
    component: AdminProductForm,
    name: 'admin-product-edit',
    meta: { requiresStaff: true },
  },
  { path: '/', component: HomePage, name: 'home' },
]

export const router = createRouter({
  history: createWebHistory(), // update url depending on the path
  routes,
})

// Route guard for staff-only routes
router.beforeEach((to, from, next) => {
  if (to.meta.requiresStaff) {
    const authStore = useAuthStore()
    if (!authStore.isAuthenticated || !authStore.isStaff) {
      // Redirect non-staff users to home
      next({ name: 'home' })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
