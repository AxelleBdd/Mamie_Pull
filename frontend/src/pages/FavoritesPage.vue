<template>
  <h1
    class="text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight"
  >
    <u>Mes favoris</u>
  </h1>
  <div class="favorites-container flex flex-col items-center gap-6 mt-6">
    <div v-if="loading" class="loading">Chargement...</div>
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    <div
      v-else-if="favorites.length === 0"
      class="flex flex-col items-center gap-4"
    >
      <p>Vous n'avez aucun favori pour le moment.</p>
      <router-link
        class="bg-dark-purple text-white-purple hover:bg-highlight-purple py-2 px-4 rounded-lg text-center sg:w-30 lg:w-40"
        :to="{ path: '/products' }"
      >
        Explorer le catalogue
      </router-link>
    </div>
    <div
      v-else
      class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 w-full px-4"
    >
      <div v-for="product in favorites" :key="product.id" class="relative">
        <ProductCard
          :product="product"
          role="listitem"
          @view-details="viewProductDetails"
        />
        <FavoriteButton
          :product-id="product.id"
          class="absolute top-4 right-4"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { router } from '../router'
import { useFavoriteStore } from '../stores/favoriteStore'
import { useAuthStore } from '../stores/authStore'
import { storeToRefs } from 'pinia'

import ButtonDark from '../components/ButtonDark.vue'
import ProductCard from '../components/ProductCard.vue'
import FavoriteButton from '../components/FavoriteButton.vue'

const authStore = useAuthStore()
const favoriteStore = useFavoriteStore()
const { favorites, loading, error } = storeToRefs(favoriteStore)

const viewProductDetails = (productId) => {
  router.push(`/products/${productId}`)
}

watch(
  () => authStore.isInitialized,
  (initialized) => {
    if (initialized) favoriteStore.fetchFavorites()
  },
  { immediate: true },
)
</script>
