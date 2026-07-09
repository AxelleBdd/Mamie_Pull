<template>
  <button
    class="w-10 h-10 rounded-full bg-white-purple flex items-center justify-center shadow-md hover:cursor-pointer hover:bg-white transition"
    :aria-label="isFav ? 'Retirer des favoris' : 'Ajouter aux favoris'"
    @click.prevent="toggle"
  >
    <Heart v-if="isFav" fill="currentColor" />
    <Heart v-else />
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useFavoriteStore } from '../stores/favoriteStore'
import { Heart } from '@lucide/vue'

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
