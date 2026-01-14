import { createPinia } from 'pinia'
import type { Pinia } from 'pinia'

export default defineNuxtPlugin((nuxtApp) => {
  const pinia: Pinia = createPinia()
  nuxtApp.vueApp.use(pinia)
})
