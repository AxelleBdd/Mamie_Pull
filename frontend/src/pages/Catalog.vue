<template>
  <div
    class="max-w-400 mx-auto px-4 md:px-8 lg:px-12 py-4 bg-white-purple-100"
  >
    <!-- Header -->
    <header class="text-center mb-4">
      <h1
        class="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading text-dark-purple-700 mb-2"
      >
        Catalogue de produits
      </h1>
      <p class="text-base sm:text-lg md:text-xl font-body text-dark-purple-700">
        Découvrez notre collection de produits faits main avec amour
      </p>
    </header>

    <!-- Breadcrumb -->
    <nav
      aria-label="Fil d'Ariane"
      class="mb-6 flex items-center gap-2 sm:text-lg md:text-xl text-dark-purple-700"
    >
      <router-link to="/" class="hover:underline">Accueil</router-link>
      <span aria-hidden="true"> > </span>
      <span aria-current="page" class="font-medium">Produits</span>
    </nav>

    <!-- Filters -->
    <div
      v-if="categories.length > 0"
      class="flex flex-wrap justify-center gap-3 mb-4 p-6 bg-white-purple-100 rounded-xl"
    >
      <button
        class="px-5 py-2 rounded-full border-2 text-sm md:text-base font-medium transition border-dark-purple-700 hover:cursor-pointer"
        :class="{
          'bg-dark-purple-700 text-white hover:text-grey-purple-400':
            selectedCategory === null,
          'bg-white-purple-100 text-dark-purple-700 hover:text-dark-purple-700 hover:bg-grey-purple-400':
            selectedCategory !== null,
        }"
        aria-label="Afficher tous les produits"
        :aria-pressed="selectedCategory === null"
        @click="filterByCategory(null)"
      >
        Tous les produits ({{ products.length }})
      </button>

      <button
        v-for="category in categories"
        :key="category.id"
        class="px-5 py-2 rounded-full border-2 text-sm md:text-base font-medium transition border-dark-purple-700 hover:cursor-pointer"
        :class="{
          'bg-dark-purple-700 text-white-purple-100 hover:text-grey-purple-400':
            selectedCategory === category.id,
          'bg-white-purple-100 text-dark-purple-700 hover:text-dark-purple-700 hover:bg-grey-purple-400':
            selectedCategory !== category.id,
        }"
        :aria-label="`Filtrer par la catégorie ${category.name}`"
        :aria-pressed="selectedCategory === category.id"
        @click="filterByCategory(category.id)"
      >
        {{ category.name }} ({{ getCategoryCount(category.id) }})
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16">
      <div
        class="mx-auto mb-4 h-12 w-12 rounded-full border-4 border-purple-200 border-t-purple-500 animate-spin"
      ></div>
      <p class="text-lg text-purple-300">Chargement des produits...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" role="alert" class="text-center py-16">
      <span aria-hidden="true" class="text-6xl mb-4 block">⚠️</span>
      <h3 class="text-2xl font-semibold text-dark-purple-700 mb-2">
        Erreur de chargement
      </h3>
      <p class="text-light-purple-300 mb-6">
        {{ error }}
      </p>
      <button
        class="px-8 py-3 rounded-lg font-medium text-white bg-purple-500 hover:bg-purple-700 transition"
        @click="loadProducts"
      >
        Réessayer
      </button>
    </div>

    <!-- Products -->
    <div
      v-else-if="filteredProducts.length > 0"
      role="list"
      aria-label="Liste des produits de la catégorie"
      class="grid gap-8 grid-cols-[repeat(auto-fill,minmax(300px,1fr))]"
    >
      <ProductCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        role="listitem"
        @view-details="viewProductDetails"
      />
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-16">
      <span aria-hidden="true" class="text-6xl mb-4 block opacity-50">📦</span>
      <h3 class="text-2xl font-semibold text-dark-purple-700 mb-2">
        Aucun produit trouvé
      </h3>
      <p class="text-highlight-purple-500">
        Il n'y a pas encore de produits dans cette catégorie.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import { getAllProducts } from '../api/products.js'

const products = ref([])
const loading = ref(true)
const error = ref(null)
const selectedCategory = ref(null)

// Get categories from products
const categories = computed(() => {
  const uniqueCategories = new Map()
  products.value.forEach((product) => {
    if (!uniqueCategories.has(product.category)) {
      uniqueCategories.set(product.category, {
        id: product.category,
        name: product.category_name,
      })
    }
  })
  return Array.from(uniqueCategories.values()).sort((a, b) =>
    a.name.localeCompare(b.name),
  )
})

// Category filtering
const filteredProducts = computed(() => {
  if (selectedCategory.value === null) {
    return products.value
  }
  return products.value.filter(
    (product) => product.category === selectedCategory.value,
  )
})

// Count products in a category
const getCategoryCount = (categoryId) => {
  return products.value.filter((product) => product.category === categoryId)
    .length
}

// Filter by category
const filterByCategory = (categoryId) => {
  selectedCategory.value = categoryId
}

// Load products from API
const loadProducts = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await getAllProducts()
    products.value = data
  } catch (err) {
    error.value =
      'Impossible de charger les produits. Vérifiez que le backend est bien lancé.'
    console.error('Erreur de chargement:', err)
  } finally {
    loading.value = false
  }
}

// See product details
const viewProductDetails = (productId) => {
  console.log('Voir les détails du produit:', productId)
  // TODO: Add navigation to product details page
  // router.push(`/products/${productId}`);
}

// Load products on component mount
onMounted(() => {
  loadProducts()
})
</script>
