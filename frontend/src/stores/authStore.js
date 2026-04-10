import { defineStore } from 'pinia'
import { loginRequest, signupRequest } from '../api/authService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Access token in memory only - lost on page refresh
    accessToken: null,
  }),

  getters: {
    isAuthenticated: (state) => state.accessToken !== null,
  },

  actions: {
    async login(email, password) {
      const { access, refresh } = await loginRequest(email, password)

      // Stock access token in Pinia
      this.accessToken = access
      // Refresh token in localStorage
      localStorage.setItem('refreshToken', refresh)
    },

    logout() {
      this.accessToken = null
      localStorage.removeItem('refreshToken')
    },

    async signup(signupData) {
      await signupRequest(signupData)
      // After successful signup, auto-login the user
      const { access, refresh } = await loginRequest(
        signupData.email,
        signupData.password,
      )
      this.accessToken = access
      localStorage.setItem('refreshToken', refresh)
    },
  },
})
