import { createMemoryHistory, createRouter } from 'vue-router'

import Catalog from '../pages/Catalog.vue'

const routes = [
  { path: '/products', component: Catalog },
]

export const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;