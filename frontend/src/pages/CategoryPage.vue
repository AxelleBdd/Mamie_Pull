<template>
  <div
    class="max-w-400 mx-auto px-4 md:px-8 lg:px-12 py-4 bg-white-purple text-dark-purple"
  >
    <!-- Header -->
    <header class="text-center mb-4">
      <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading mb-2">
        {{ currentCategory?.name || 'Catégorie' }}
      </h1>
      <p class="text-base sm:text-lg md:text-xl font-body">
        Découvrez nos produits faits main avec amour
      </p>
    </header>

    <!-- Breadcrumb -->
    <nav
      aria-label="Fil d'Ariane"
      class="mb-6 flex items-center gap-2 sm:text-lg md:text-xl font-body"
    >
      <router-link to="/" class="hover:underline">Accueil</router-link>
      <span aria-hidden="true"> > </span>
      <router-link to="/products" class="hover:underline">Produits</router-link>
      <span aria-hidden="true"> > </span>
      <span aria-current="page" class="font-medium">{{
        currentCategory?.name
      }}</span>
    </nav>

    <!-- Loading -->
    <div v-if="loading" role="status" class="text-center py-16">
      <p class="text-lg text-light-purple">Chargement des produits...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" role="alert" class="text-center py-16">
      <span aria-hidden="true" class="text-6xl mb-4 block">⚠️</span>
      <h3 class="text-2xl font-semibold mb-2">Erreur de chargement</h3>
      <p class="text-light-purple mb-6">
        {{ error }}
      </p>
    </div>

    <!-- Category not found -->
    <div v-else-if="!currentCategory" role="alert" class="text-center py-16">
      <span aria-hidden="true" class="text-6xl mb-4 block">🔍</span>
      <h3 class="text-2xl font-semibold mb-2">Catégorie introuvable</h3>
      <p class="text-highlight-purple mb-6">
        La catégorie demandée n'existe pas.
      </p>
      <router-link
        to="/products"
        aria-label="Retourner à la page de tous les produits"
        class="inline-block px-8 py-3 rounded-lg font-medium text-white-purple bg-dark-purple hover:bg-purple transition"
      >
        Voir tous les produits
      </router-link>
    </div>

    <!-- Products -->
    <div
      v-else-if="products.length > 0"
      role="list"
      aria-label="Liste des produits de la catégorie"
      class="grid gap-8 grid-cols-[repeat(auto-fill,minmax(300px,1fr))]"
    >
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
        role="listitem"
        @view-details="viewProductDetails"
      />
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-16">
      <span aria-hidden="true" class="text-6xl mb-4 block opacity-50">📦</span>
      <h3 class="text-2xl font-semibold mb-2">Aucun produit trouvé</h3>
      <p class="text-highlight-purple mb-6">
        Il n'y a pas encore de produits dans cette catégorie.
      </p>
      <router-link
        to="/products"
        aria-label="Retourner à la page de tous les produits"
        class="inline-block px-8 py-3 rounded-lg font-medium text-white-purple bg-dark-purple hover:bg-purple transition"
      >
        Voir tous les produits
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router' // Read route info
import { useRouter } from 'vue-router' // For navigation
import { getProductsByCategory } from '../api/products.js'
import { useCategoryStore } from '../stores/categoryStore'
import ProductCard from '../components/ProductCard.vue'

const router = useRouter()
const route = useRoute()
const categoryStore = useCategoryStore()

const products = ref([])
const loading = ref(true)
const error = ref(null)

// Get current category from slug
const currentCategory = computed(() => {
  const slug = route.params.slug
  return categoryStore.categories.find((cat) => cat.slug === slug)
})

// Load products filtered by category
const loadCategoryProducts = async () => {
  loading.value = true
  error.value = null

  try {
    if (currentCategory.value) {
      products.value = await getProductsByCategory(currentCategory.value.id)
    } else {
      products.value = []
    }
  } catch (err) {
    error.value = 'Impossible de charger les produits.'
    console.error('Erreur de chargement:', err)
  } finally {
    loading.value = false
  }
}

// See product details
const viewProductDetails = (productId) => {
  router.push(`/products/${productId}`)
}

// Watch for route changes (when navigating between categories)
watch(
  () => route.params.slug,
  () => {
    if (route.name === 'category') {
      loadCategoryProducts()
    }
  },
)

// Load on mount
onMounted(async () => {
  // Ensure categories are loaded
  if (categoryStore.categories.length === 0) {
    await categoryStore.fetchCategories()
  }
  loadCategoryProducts()
})
</script>
