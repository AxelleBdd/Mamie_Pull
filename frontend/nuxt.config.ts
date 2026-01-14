export default defineNuxtConfig({
  typescript: {strict: true},
  modules: ['@pinia/nuxt'],
    runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000/api'
    }
  }
})