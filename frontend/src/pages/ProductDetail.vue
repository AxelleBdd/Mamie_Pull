<template>
  <div
    class="max-w-400 mx-auto px-4 md:px-8 lg:px-12 py-4 bg-white-purple min-h-screen"
  >
    <!-- Header -->
    <header class="text-center mb-4">
      <h1
        class="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading text-dark-purple mb-2"
      >
        {{ product?.title || 'Chargement...' }}
      </h1>
    </header>

    <!-- Breadcrumb -->
    <nav
      aria-label="Fil d'Ariane"
      class="mb-6 flex items-center gap-2 sm:text-lg md:text-xl"
    >
      <router-link to="/" class="hover:underline">Accueil</router-link>
      <span aria-hidden="true"> > </span>
      <router-link to="/products" class="hover:underline"
        >Tous nos produits</router-link
      >
      <span aria-hidden="true"> > </span>
      <router-link
        v-if="product && product.category"
        :to="`/categories/${getCategorySlug(product.category)}`"
        class="hover:underline"
      >
        {{ product.category_name }}
      </router-link>
      <span v-if="product && product.category" aria-hidden="true"> > </span>
      <span class="font-medium" aria-current="page">{{
        product?.title || 'Chargement...'
      }}</span>
    </nav>

    <!-- Back button -->
    <ButtonDark
      class="mb-6 inline-flex items-center gap-2 rounded-lg text-lg hover:bg-highlight-purple transition lg:w-auto"
      aria-label="Retour à la page précédente"
      button-type="button"
      @click="goBack"
    >
      <svg
        class="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 19l-7-7 7-7"
        />
      </svg>
      Retour
    </ButtonDark>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16" role="status">
      <p class="text-lg text-purple">Chargement du produit...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-16" role="alert">
      <span class="text-6xl mb-4 block" aria-hidden="true">⚠️</span>
      <h2 class="text-2xl font-semibold text-purple mb-2">
        Erreur de chargement
      </h2>
      <p class="text-purple mb-6">
        {{ error }}
      </p>
    </div>

    <!-- Product Detail -->
    <div
      v-else-if="product"
      class="flex flex-col lg:flex-row gap-10 px-8 sm:px-16 md:px-24 lg:px-6 xl:px-12 2xl:px-32"
    >
      <!-- Left Column: Image -->
      <div class="lg:w-1/2">
        <div class="sticky top-4">
          <!-- Main Image with Heart -->
          <div
            class="relative rounded-xl overflow-hidden bg-grey-purple aspect-square flex items-center justify-center w-full"
          >
            <img
              v-if="product.image"
              :src="product.image"
              :alt="product.title"
              class="w-full h-full object-cover"
            />
            <span
              v-else
              class="text-9xl text-grey-purple"
              aria-hidden="true"
            >
              📦
            </span>

            <!-- Heart Icon -->
            <button
              class="absolute top-4 right-4 w-10 h-10 rounded-full bg-white-purple flex items-center justify-center shadow-md hover:bg-white transition"
              aria-label="Ajouter aux favoris"
              disabled
            >
              <svg
                class="w-6 h-6 text-dark-purple"
                fill="none"
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
          </div>
        </div>
      </div>

      <!-- Right Column: Details -->
      <div class="lg:w-1/2 flex flex-col lg:justify-center">
        <!-- Description Section -->
        <div class="mb-8">
          <h2 class="text-3xl font-semibold font-heading mb-4">Description</h2>
          <p class="text-base sm:text-lg md:text-xl">
            {{ product.description }}
          </p>
        </div>

        <div class="mb-8">
          <h2 class="text-3xl font-semibold font-heading mb-4">Tailles</h2>
          <div class="grid grid-cols-2 gap-2">
            <label
              v-for="size in product.sizes"
              :key="`checkbox-${size}`"
              class="inline-flex items-center gap-2 text-base sm:text-lg md:text-xl"
            >
              <input
                v-model="selectedSizes"
                type="checkbox"
                :value="size"
                class="rounded border-grey-purple text-dark-purple focus:ring-highlight-purple"
              />
              {{ size }}
            </label>
          </div>
        </div>

        <!-- Contact Button -->
        <div class="flex justify-center">
          <ButtonDark
            class="lg:w-90 py-2 px-6 rounded-lg sm:text-lg md:text-xl hover:bg-highlight-purple transition"
            aria-label="Nous contacter pour ce modèle"
            disabled
            button-type="button"
          >
            Nous contacter pour ce modèle
          </ButtonDark>
        </div>
      </div>
    </div>

    <!-- Product not found -->
    <div v-else class="text-center py-16" role="alert">
      <span class="text-6xl mb-4 block" aria-hidden="true">🔍</span>
      <h2 class="text-2xl font-semibold text-dark-purple mb-2">
        Produit introuvable
      </h2>
      <p class="text-highlight-purple mb-6">
        Le produit demandé n'existe pas ou a été supprimé.
      </p>
      <router-link
        to="/products"
        class="inline-block px-8 py-3 rounded-lg font-medium text-white bg-dark-purple hover:bg-highlight-purple transition"
        aria-label="Retourner à la page de tous les produits"
      >
        Voir tous les produits
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ButtonDark from '../components/ButtonDark.vue'
import { getProductById } from '../api/products.js'
import { useCategoryStore } from '../stores/categoryStore'

const route = useRoute()
const router = useRouter()
const categoryStore = useCategoryStore()

const product = ref(null)
const loading = ref(true)
const error = ref(null)
const selectedSizes = ref([])

// Load product details
const loadProduct = async () => {
  loading.value = true
  error.value = null

  try {
    const productId = route.params.id
    product.value = await getProductById(productId)
  } catch (err) {
    error.value =
      'Impossible de charger le produit. Vérifiez que le backend est bien lancé.'
    console.error('Erreur de chargement:', err)
  } finally {
    loading.value = false
  }
}

// Get category slug from category ID
const getCategorySlug = (categoryId) => {
  const category = categoryStore.categories.find((cat) => cat.id === categoryId)
  return category?.slug || ''
}

// Go back to previous page
const goBack = () => {
  router.back()
}

// Load on mount
onMounted(async () => {
  // Ensure categories are loaded for breadcrumb
  if (categoryStore.categories.length === 0) {
    await categoryStore.fetchCategories()
  }
  loadProduct()
})
</script>
