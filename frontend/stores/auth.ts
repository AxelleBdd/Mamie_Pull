import { defineStore } from 'pinia'
import { $fetch } from 'ofetch'


interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
}

interface LoginResponse {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: null,
    refreshToken: null,
    isAuthenticated: false
  }),

  actions: {
    async login(email: string, password: string): Promise<void> {
      const response = await $fetch<LoginResponse>('http://backend:8000/api/login/', {
        method: 'POST',
        body: { email, password }
      })

      this.accessToken = response.access
      this.refreshToken = response.refresh
      this.isAuthenticated = true

      localStorage.setItem('access', response.access)
      localStorage.setItem('refresh', response.refresh)
    },

    logout(): void {
      this.accessToken = null
      this.refreshToken = null
      this.isAuthenticated = false

      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    },

    loadTokens(): void {
      const access = localStorage.getItem('access')
      const refresh = localStorage.getItem('refresh')

      if (access && refresh) {
        this.accessToken = access
        this.refreshToken = refresh
        this.isAuthenticated = true
      }
    }
  }
})
