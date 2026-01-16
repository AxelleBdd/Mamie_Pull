<template>
  <div class="max-w-[1400px] mx-auto px-4 py-8 bg-white-purple-100">
    <!-- Header -->
    <header class="text-center mb-12">
      <h1 class="text-4xl font-bold font-heading text-dark-purple-700 font-heading mb-2">
        Catalogue de produits
      </h1>
      <p class="text-lg text-dark-purple-700 font-body">
        Découvrez notre collection de produits faits main avec amour
      </p>
    </header>

    <!-- Filters -->
    <div
      v-if="categories.length > 0"
      class="flex flex-wrap justify-center gap-3 mb-10 p-6 bg-white-purple-100 rounded-xl"
    >
      <button
        @click="filterByCategory(null)"
        class="px-5 py-2 rounded-full border-2 text-sm transition
          border-dark-purple-700 text-dark-purple-700
          hover:border-highlight-purple-500 hover:text-highlight-purple-500"
        :class="selectedCategory === null
          ? 'bg-dark-purple-700 border-dark-purple-700 text-white'
          : 'bg-white'"
      >
        Tous les produits ({{ products.length }})
      </button>

      <button
        v-for="category in categories"
        :key="category.id"
        @click="filterByCategory(category.id)"
        class="px-5 py-2 rounded-full border-2 text-sm font-medium transition
          border-dark-purple-700 text-dark-purple-700
          hover:border-dark-purple-700 hover:text-highlight-purple-500"
        :class="selectedCategory === category.id
          ? 'bg-dark-purple-700 border-dark-purple-700 text-white-purple-100'
          : 'bg-white'"
      >
        {{ category.name }} ({{ getCategoryCount(category.id) }})
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-16">
      <div
        class="mx-auto mb-4 h-12 w-12 rounded-full border-4 border-purple-200 border-t-purple-500 animate-spin"
      ></div>
      <p class="text-lg text-purple-300">
        Chargement des produits...
      </p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-16">
      <span class="text-6xl mb-4 block">⚠️</span>
      <h3 class="text-2xl font-semibold text-purple-900 mb-2">
        Erreur de chargement
      </h3>
      <p class="text-purple-300 mb-6">
        {{ error }}
      </p>
      <button
        @click="loadProducts"
        class="px-8 py-3 rounded-lg font-medium text-white bg-purple-500
               hover:bg-purple-700 transition"
      >
        Réessayer
      </button>
    </div>

    <!-- Products -->
    <div
      v-else-if="filteredProducts.length > 0"
      class="grid gap-8 grid-cols-[repeat(auto-fill,minmax(300px,1fr))]"
    >
      <ProductCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        @view-details="viewProductDetails"
      />
    </div>

    <!-- Empty -->
    <div v-else class="text-center py-16">
      <span class="text-6xl mb-4 block opacity-50">📦</span>
      <h3 class="text-2xl font-semibold text-purple-700 mb-2">
        Aucun produit trouvé
      </h3>
      <p class="text-purple-300">
        Il n'y a pas encore de produits dans cette catégorie.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import ProductCard from '../components/ProductCard.vue';
import { getAllProducts } from '../api/products.js';

const products = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedCategory = ref(null);

// Récupérer les catégories uniques des produits
const categories = computed(() => {
  const uniqueCategories = new Map();
  products.value.forEach(product => {
    if (!uniqueCategories.has(product.category)) {
      uniqueCategories.set(product.category, {
        id: product.category,
        name: product.category_name
      });
    }
  });
  return Array.from(uniqueCategories.values()).sort((a, b) => a.name.localeCompare(b.name));
});

// Category filtering
const filteredProducts = computed(() => {
  if (selectedCategory.value === null) {
    return products.value;
  }
  return products.value.filter(product => product.category === selectedCategory.value);
});

// Count products in a category
const getCategoryCount = (categoryId) => {
  return products.value.filter(product => product.category === categoryId).length;
};

// Filter by category
const filterByCategory = (categoryId) => {
  selectedCategory.value = categoryId;
};

// Load products from API
const loadProducts = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const data = await getAllProducts();
    products.value = data;
  } catch (err) {
    error.value = 'Impossible de charger les produits. Vérifiez que le backend est bien lancé.';
    console.error('Erreur de chargement:', err);
  } finally {
    loading.value = false;
  }
};

// See product details
const viewProductDetails = (productId) => {
  console.log('Voir les détails du produit:', productId);
  // TODO: Add navigation to product details page
  // router.push(`/products/${productId}`);
};

// Load products on component mount
onMounted(() => {
  loadProducts();
});
</script>