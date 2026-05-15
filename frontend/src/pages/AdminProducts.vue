<template>
  <div class="max-w-6xl mx-auto px-6 py-8">
    <h1
      class="text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight"
    >
      <u>Admin - Gestion des Produits</u>
    </h1>

    <!-- Messages -->
    <div
      v-if="successMessage"
      class="border border-light-purple bg-white-purple px-4 py-3 rounded mb-4 text-highlight-purple"
    >
      {{ successMessage }}
    </div>
    <div
      v-if="errorMessage"
      class="border border-error-purple bg-white-purple text-error-purple px-4 py-3 rounded mb-4"
    >
      {{ errorMessage }}
    </div>

    <!-- Add button -->
    <router-link
      to="/admin/products/new"
      class="bg-highlight-purple hover:bg-dark-purple text-white font-semibold py-2 px-4 rounded my-6 transition inline-block"
    >
      + Ajouter un produit
    </router-link>

    <!-- Products table (Desktop) -->
    <div v-if="loading" class="text-center py-12 text-light-purple text-lg">
      Chargement des produits...
    </div>

    <div
      v-if="products.length > 0"
      class="hidden md:block overflow-x-auto rounded-lg shadow"
    >
      <table class="w-full bg-white border-collapse">
        <thead class="bg-grey-purple border-b-2 border-light-purple">
          <tr>
            <th class="px-4 py-3 text-left font-semibold">Titre</th>
            <th class="px-4 py-3 text-left font-semibold">Description</th>
            <th class="px-4 py-3 text-left font-semibold">Catégorie</th>
            <th class="px-4 py-3 text-left font-semibold">Tailles</th>
            <th class="px-4 py-3 text-left font-semibold">Créé par</th>
            <th class="px-4 py-3 text-left font-semibold">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="product in paginatedProducts"
            :key="product.id"
            class="border-b border-grey-purple hover:bg-white-purple"
          >
            <td class="px-4 py-3">{{ product.title }}</td>
            <td class="px-4 py-3 max-w-xs wrap-break-words text-sm">
              {{ truncateText(product.description, 50) }}
            </td>
            <td class="px-4 py-3">{{ product.category_name }}</td>
            <td class="px-4 py-3 text-sm">{{ formatSizes(product.sizes) }}</td>
            <td class="px-4 py-3">{{ product.created_by_name || 'N/A' }}</td>
            <td class="px-4 py-3">
              <div class="flex gap-2">
                <router-link
                  :to="`/admin/products/${product.id}/edit`"
                  class="bg-highlight-purple hover:bg-dark-purple text-white py-1 px-3 rounded self-center text-sm transition"
                >
                  Editer
                </router-link>
                <button
                  class="bg-grey-purple text-dark-purple hover:bg-dark-purple hover:text-white-purple py-1 px-3 rounded text-sm transition"
                  @click="deleteProductHandler(product.id)"
                >
                  Supprimer
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Products cards (Mobile) -->
    <div v-if="products.length > 0" class="md:hidden space-y-3">
      <div
        v-for="product in paginatedProducts"
        :key="product.id"
        class="bg-white-purple rounded-lg p-4 border border-light-purple"
      >
        <div class="flex flex-col">
          <div class="mb-4">
            <h3 class="font-semibold text-lg text-dark-purple mb-2">
              {{ product.title }}
            </h3>
            <p class="text-sm text-dark-purple">
              {{ product.category_name }}
            </p>
          </div>
          <div class="flex gap-2 justify-between">
            <button
              class="bg-grey-purple text-dark-purple hover:bg-dark-purple hover:text-white-purple py-1 px-3 rounded text-sm transition text-center flex-1"
              @click="deleteProductHandler(product.id)"
            >
              Supprimer
            </button>
            <router-link
              :to="`/admin/products/${product.id}/edit`"
              class="bg-highlight-purple hover:bg-dark-purple text-white py-1 px-3 rounded text-sm transition text-center flex-1"
            >
              Editer
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="totalPages > 1"
      class="flex flex-wrap justify-center items-center gap-2 mt-4"
    >
      <button
        class="px-3 py-2 rounded bg-grey-purple text-dark-purple hover:bg-dark-purple hover:text-white-purple transition disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="currentPage === 1"
        @click="gotoPage(currentPage - 1)"
      >
        Précédent
      </button>
      <button
        v-for="page in totalPages"
        :key="page"
        class="px-3 py-2 rounded transition"
        :class="
          page === currentPage
            ? 'bg-highlight-purple text-white'
            : 'bg-white border border-grey-purple text-dark-purple hover:bg-grey-purple'
        "
        @click="gotoPage(page)"
      >
        {{ page }}
      </button>
      <button
        class="px-3 py-2 rounded bg-grey-purple text-dark-purple hover:bg-dark-purple hover:text-white-purple transition disabled:opacity-50 disabled:cursor-not-allowed"
        :disabled="currentPage === totalPages"
        @click="gotoPage(currentPage + 1)"
      >
        Suivant
      </button>
    </div>
    <p
      v-if="!loading && products.length === 0"
      class="mb-4 text-center py-12 text-light-purple"
    >
      Aucun produit trouvé.
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useCategoryStore } from '../stores/categoryStore'
import {
  getAllProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from '../api/products'

const authStore = useAuthStore()
const categoryStore = useCategoryStore()

const products = ref([])
const loading = ref(false)
const showForm = ref(false)
const isEditing = ref(false)
const successMessage = ref('')
const errorMessage = ref('')
const editingProductId = ref(null)
const currentPage = ref(1)

const ITEMS_PER_PAGE = 12

const formData = ref({
  title: '',
  description: '',
  category: '',
  sizes: [],
  sizesText: '',
  image: '',
})

const categories = computed(() => categoryStore.categories)

onMounted(async () => {
  await loadProducts()
  await categoryStore.fetchCategories()
})

async function loadProducts() {
  try {
    loading.value = true
    const data = await getAllProducts()
    products.value = data
    currentPage.value = 1
  } catch (error) {
    showError('Erreur lors du chargement des produits: ' + error.message)
  } finally {
    loading.value = false
  }
}

function openAddForm() {
  isEditing.value = false
  editingProductId.value = null
  resetForm()
  showForm.value = true
}

function openEditForm(product) {
  isEditing.value = true
  editingProductId.value = product.id
  formData.value = {
    title: product.title,
    description: product.description,
    category: product.category,
    sizes: product.sizes,
    sizesText: JSON.stringify(product.sizes),
    image: product.image || '',
  }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  resetForm()
}

function resetForm() {
  formData.value = {
    title: '',
    description: '',
    category: '',
    sizes: [],
    sizesText: '',
    image: '',
  }
}

function parseSizes() {
  try {
    if (formData.value.sizesText.trim()) {
      formData.value.sizes = JSON.parse(formData.value.sizesText)
    } else {
      formData.value.sizes = []
    }
    return true
  } catch (error) {
    showError('Format de tailles invalide. Utilisez un format JSON valide.')
    return false
  }
}

function formatSizes(sizes) {
  if (!sizes || sizes.length === 0) return '-'
  return sizes.join(', ')
}

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(products.value.length / ITEMS_PER_PAGE))
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * ITEMS_PER_PAGE
  return products.value.slice(start, start + ITEMS_PER_PAGE)
})

function gotoPage(page) {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}

function truncateText(text, length) {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

async function submitForm() {
  if (!parseSizes()) return

  try {
    const payload = {
      title: formData.value.title,
      description: formData.value.description,
      category: formData.value.category,
      sizes: formData.value.sizes,
    }
    if (formData.value.image) {
      payload.image = formData.value.image
    }

    if (isEditing.value) {
      await updateProduct(
        editingProductId.value,
        payload,
        authStore.accessToken,
      )
      showSuccess('Produit mis à jour avec succès')
    } else {
      await createProduct(payload, authStore.accessToken)
      showSuccess('Produit créé avec succès')
    }

    closeForm()
    await loadProducts()
  } catch (error) {
    showError('Erreur: ' + error.message)
  }
}

async function deleteProductHandler(productId) {
  if (confirm('Êtes-vous sûr de vouloir supprimer ce produit?')) {
    try {
      await deleteProduct(productId, authStore.accessToken)
      showSuccess('Produit supprimé avec succès')
      await loadProducts()
    } catch (error) {
      showError('Erreur: ' + error.message)
    }
  }
}

function showSuccess(message) {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

function showError(message) {
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 5000)
}
</script>
