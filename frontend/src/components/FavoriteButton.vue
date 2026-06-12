<template>
  <button
    class="w-10 h-10 rounded-full bg-white-purple flex items-center justify-center shadow-md hover:cursor-pointer hover:bg-white transition"
    :aria-label="isFav ? 'Retirer des favoris' : 'Ajouter aux favoris'"
    @click.prevent="toggle"
  >
    <svg
      class="w-6 h-6 transition-colors"
      :fill="isFav ? 'currentColor' : 'none'"
      :class="isFav ? 'text-dark-purple' : 'text-dark-purple'"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
      />
    </svg>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useFavoriteStore } from '../stores/favoriteStore'

const props = defineProps({
  productId: {
    type: Number,
    required: true,
  },
})

const router = useRouter()
const authStore = useAuthStore()
const favoriteStore = useFavoriteStore()

const isFav = computed(() => favoriteStore.isFavorite(props.productId))

const toggle = async () => {
  if (!authStore.isInitialized) return
  try {
    if (isFav.value) {
      await favoriteStore.removeFavorite(props.productId)
    } else {
      await favoriteStore.addFavorite(props.productId)
    }
  } catch (err) {
    console.error('Erreur favoris:', err)
    alert('Une erreur est survenue. Veuillez réessayer.')
  }
}
</script>
