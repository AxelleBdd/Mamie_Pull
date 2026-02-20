import { defineStore } from 'pinia'

export const useSessionStore = defineStore('session', {
  state: () => ({
    user: null
  }),

  getters: {
    isLoggedIn: (state) => !!state.user
  },

  actions: {
    async login(username, password) {
      // Simulated delay
      await new Promise(resolve => setTimeout(resolve, 500))

      // Simulated user credentials
      if (username === 'admin' && password === 'password') {
        this.user = { name: 'Admin', id: 1 }
        sessionStorage.setItem('user', JSON.stringify(this.user))
        return true
      }

      return false
    },

    logout() {
      this.user = null
      sessionStorage.removeItem('user')
    },

    loadSession() {
      const data = sessionStorage.getItem('user')
      if (data) {
        this.user = JSON.parse(data)
      }
    }
  }
})