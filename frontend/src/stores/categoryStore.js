import { defineStore } from 'pinia'
import { ref } from 'vue'

const API_BASE_URL = 'http://localhost:8000/api';

export const useCategoryStore = defineStore('category', () => {
  const categories = ref([])
  const loading = ref(false)
  const error = ref(null)

  // GET Categories
  async function fetchCategories() {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${API_BASE_URL}/categories/`)
      if (!response.ok) throw new Error('Erreur lors du chargement')
      
      const data = await response.json()
      categories.value = data
    } catch (e) {
      error.value = e.message
      console.error('Erreur catégories:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    categories,
    loading,
    error,
    fetchCategories
  }
})