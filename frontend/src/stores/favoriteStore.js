import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useAuthStore } from './authStore'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const useFavoriteStore = defineStore('favorite', () => {
  const favorites = ref([])
  const loading = ref(false)
  const error = ref(null)

  // GET Favorites
  async function fetchFavorites() {
    const authStore = useAuthStore()
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/favorites/`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authStore.accessToken}`,
        },
      })
      if (!response.ok) throw new Error('Erreur lors du chargement')

      const data = await response.json()
      favorites.value = data
    } catch (e) {
      error.value = e.message
      console.error('Erreur favoris:', e)
    } finally {
      loading.value = false
    }
  }

  // POST Favorite
  async function addFavorite(productId) {
    const authStore = useAuthStore()
    try {
      const response = await fetch(`${API_BASE_URL}/favorites/${productId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authStore.accessToken}`,
        },
      })
      if (!response.ok) throw new Error("Erreur lors de l'ajout")
      // remove from local state immediately
      const product = await response.json()
      favorites.value.push(product)
    } catch (e) {
      console.error('Erreur ajout favoris:', e)
      throw e
    }
  }

  function isFavorite(productId) {
    return favorites.value.some((p) => p.id === productId)
  }

  // DELETE favorite
  async function removeFavorite(productId) {
    const authStore = useAuthStore()
    try {
      const response = await fetch(`${API_BASE_URL}/favorites/${productId}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${authStore.accessToken}`,
        },
      })
      if (!response.ok) throw new Error('Erreur lors de la suppression')
      // same as addFavorite
      favorites.value = favorites.value.filter((p) => p.id !== productId)
    } catch (e) {
      console.error('Erreur suppression favoris:', e)
      throw e
    }
  }

  return {
    favorites,
    loading,
    error,
    fetchFavorites,
    addFavorite,
    removeFavorite,
    isFavorite,
  }
})
