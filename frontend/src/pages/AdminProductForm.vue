<template>
  <div class="max-w-2xl mx-auto px-6 py-8">
    <div class="mb-6 flex justify-start -ml-8 sm:ml-0">
      <router-link to="/admin/products" aria-label="Retour à la liste">
        <div
          class="flex mb-6 items-center gap-2 rounded-lg text-lg hover:bg-highlight-purple transition lg:w-auto bg-dark-purple hover:cursor-pointer text-white-purple py-2 px-4 mx-auto sg:w-30"
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
          <p>Retour à la liste</p>
        </div>
      </router-link>
    </div>

    <h1
      class="mt-10 text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight mb-8"
    >
      <u>{{ isEditing ? `Éditer ${formData.title}` : 'Ajouter un produit' }}</u>
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

    <!-- Form Card -->
    <div
      class="bg-grey-purple rounded-lg shadow-lg p-8 border border-grey-purple"
    >
      <form @submit.prevent="submitForm">
        <div class="mb-3 sm:mb-6">
          <label
            for="title"
            class="block font-heading text-xl sm:text-3xl font-medium text-dark-purple mb-1 sm:mb-2"
          >
            Titre *
          </label>
          <input
            id="title"
            v-model="formData.title"
            type="text"
            required
            placeholder="Titre du produit"
            class="w-full px-3 py-1.5 bg-white-purple rounded-lg outline-1 -outline-offset-1 outline-dark-purple focus:outline-2 text-lg"
          />
        </div>

        <div class="mb-3 sm:mb-6">
          <label
            for="description"
            class="block font-heading text-xl sm:text-3xl font-medium text-dark-purple mb-1 sm:mb-2"
          >
            Description *
          </label>
          <textarea
            id="description"
            v-model="formData.description"
            required
            placeholder="Description du produit"
            rows="5"
            class="w-full px-3 py-1.5 bg-white-purple rounded-lg outline-1 -outline-offset-1 outline-dark-purple focus:outline-2 text-lg"
          ></textarea>
        </div>

        <div class="mb-3 sm:mb-6">
          <label
            for="category"
            class="block font-heading text-xl sm:text-3xl font-medium text-dark-purple mb-1 sm:mb-2"
          >
            Catégorie *
          </label>
          <select
            id="category"
            v-model.number="formData.category"
            required
            class="w-full px-3 py-1.5 bg-white-purple rounded-lg outline-1 -outline-offset-1 outline-dark-purple hover:cursor-pointer focus:outline-2 text-lg"
          >
            <option value="">-- Sélectionner une catégorie --</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }}
            </option>
          </select>
        </div>

        <div class="mb-3 sm:mb-6">
          <p
            class="block font-heading text-xl sm:text-3xl font-medium text-dark-purple mb-1 sm:mb-2"
          >
            Tailles
          </p>
          <div class="grid grid-cols-2 gap-2">
            <label
              v-for="size in sizeOptions"
              :key="size"
              class="flex items-center gap-2 px-3 py-2 border border-grey-purple bg-white-purple rounded-md hover:cursor-pointer hover:border-highlight-purple"
            >
              <input
                v-model="formData.sizes"
                type="checkbox"
                :value="size"
                class="h-4 w-4 text-highlight-purple focus:ring-highlight-purple hover:cursor-pointer rounded font-medium"
              />
              <span class="text-base">{{ size }}</span>
            </label>
          </div>
        </div>

        <div class="mb-3 sm:mb-8">
          <label
            for="image"
            class="block font-heading text-xl sm:text-3xl font-medium text-dark-purple mb-1 sm:mb-2"
          >
            Image (URL)
          </label>
          <input
            id="image"
            v-model="formData.image"
            type="text"
            placeholder="URL de l'image"
            class="w-full px-3 py-1.5 bg-white-purple rounded-lg outline-1 -outline-offset-1 outline-dark-purple focus:outline-2 text-lg"
          />
        </div>

        <div class="flex justify-evenly">
          <router-link
            to="/admin/products"
            class="bg-white-purple text-dark-purple hover:bg-white py-2 px-4 rounded-lg text-center sg:w-30 lg:w-40"
          >
            Annuler
          </router-link>
          <ButtonDark class="sg:w-30 lg:w-40 mx-0!" @click="submitForm">
            {{ isEditing ? 'Mettre à jour' : 'Ajouter' }}
          </ButtonDark>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { useCategoryStore } from '../stores/categoryStore'
import { getProductById, createProduct, updateProduct } from '../api/products'
import ButtonDark from '../components/ButtonDark.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const categoryStore = useCategoryStore()

const isEditing = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const formData = ref({
  title: '',
  description: '',
  category: '',
  sizes: [],
  image: '',
})

const sizeOptions = [
  'Naissance',
  '3 mois',
  '6 mois',
  '12 mois',
  '18 mois',
  '24 mois',
  '36 mois',
  '4 ans',
  '6 ans',
  '8 ans',
  'Taille unique',
]

const categories = computed(() => categoryStore.categories)

onMounted(async () => {
  await categoryStore.fetchCategories()

  // Check if editing an existing product
  if (route.params.id) {
    isEditing.value = true
    await loadProduct(route.params.id)
  }
})

async function loadProduct(productId) {
  try {
    const product = await getProductById(productId)
    formData.value = {
      title: product.title,
      description: product.description,
      category: product.category,
      sizes: product.sizes,
      image: product.image || '',
    }
  } catch (error) {
    showError('Erreur lors du chargement du produit: ' + error.message)
    setTimeout(() => {
      router.push('/admin/products')
    }, 2000)
  }
}

async function submitForm() {
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
      await updateProduct(route.params.id, payload, authStore.accessToken)
      showSuccess('Produit mis à jour avec succès')
    } else {
      await createProduct(payload, authStore.accessToken)
      showSuccess('Produit créé avec succès')
    }

    setTimeout(() => {
      router.push('/admin/products')
    }, 1500)
  } catch (error) {
    showError('Erreur: ' + error.message)
  }
}

function showSuccess(message) {
  successMessage.value = message
}

function showError(message) {
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 5000)
}
</script>
