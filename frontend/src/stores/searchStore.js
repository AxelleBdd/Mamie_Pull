import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useSearchStore = defineStore('search', () => {
  const query = ref('')

  const setQuery = (newQuery) => {
    query.value = newQuery
  }

  const clearQuery = () => {
    query.value = ''
  }

  return {
    query,
    setQuery,
    clearQuery,
  }
})
