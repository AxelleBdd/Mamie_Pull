import { defineStore } from 'pinia'
import { loginRequest, signupRequest } from '../api/authService'
import { getCurrentUser } from '../api/users'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    // Access token in memory only - lost on page refresh
    accessToken: null,
    // Current user data
    user: null,
  }),

  getters: {
    isAuthenticated: (state) => state.accessToken !== null,
    isStaff: (state) => state.user?.is_staff || false,
  },

  actions: {
    async fetchUser() {
      if (!this.accessToken) return
      try {
        const userData = await getCurrentUser(this.accessToken)
        this.user = userData
      } catch (error) {
        console.error('Failed to fetch user:', error)
      }
    },

    async login(email, password) {
      const { access, refresh } = await loginRequest(email, password)

      // Stock access token in Pinia
      this.accessToken = access
      // Refresh token in localStorage
      localStorage.setItem('refreshToken', refresh)

      // Fetch user data
      await this.fetchUser()
    },

    logout() {
      this.accessToken = null
      this.user = null
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

      // Fetch user data
      await this.fetchUser()
    },

    setUser(userData) {
      this.user = userData
    },
  },
})
