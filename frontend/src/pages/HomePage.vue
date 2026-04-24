<template>
  <div class="max-w-400 mx-auto px-4 md:px-8 lg:px-12 py-6 space-y-12">
    <!-- Latest Products -->
    <section>
      <h2 class="text-3xl font-heading mb-4 text-center">
        Nos dernières créations
      </h2>

      <div v-if="loading" class="text-center py-10">
        <div
          class="mx-auto mb-4 h-12 w-12 rounded-full border-4 border-highlight-purple animate-spin"
        ></div>
        <p class="text-base text-light-purple">
          Chargement des produits...
        </p>
      </div>

      <div v-else-if="error" class="text-center py-10 text-error-purple">
        <p class="font-semibold">Erreur : {{ error }}</p>
      </div>

      <div
        v-else-if="products.length === 0"
        class="text-center py-10 text-light-purple"
      >
        Aucun produit trouvé.
      </div>

      <div v-else class="relative flex flex-col items-center">
        <div
          class="flex justify-center items-center gap-2 px-4 lg:gap-4 w-full"
        >
          <!-- Left Arrow -->
          <button
            :disabled="currentSlide === 0"
            class="shrink-0 bg-white-purple p-3 disabled:opacity-50 disabled:cursor-not-allowed hover:cursor-pointer"
            aria-label="Produit précédent"
            @click="previousSlide"
          >
            <svg
              class="w-6 h-6"
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
          </button>

          <!-- Image Container -->
          <div class="flex flex-col items-center flex-1 max-w-2xl">
            <div
              class="rounded-3xl overflow-hidden bg-grey-purple aspect-4/5 w-full max-w-lg lg:max-w-none lg:w-1/2 border border-grey-purple flex items-center justify-center"
            >
              <span class="text-3xl text-dark-purple">Image</span>
            </div>

            <!-- Dots indicator -->
            <div class="flex justify-center mt-5 gap-3">
              <div
                v-for="(product, index) in latestProducts.slice(0, 3)"
                :key="product.id"
                class="w-3 h-3 rounded-full transition-all duration"
                :class="
                  index === currentSlide
                    ? 'bg-dark-purple'
                    : 'bg-grey-purple hover:bg-grey-purple'
                "
                :aria-label="`Aller au produit ${index + 1}`"
              ></div>
            </div>
          </div>

          <!-- Right Arrow -->
          <button
            :disabled="currentSlide === latestProducts.slice(0, 3).length - 1"
            class="shrink-0 bg-white-purple p-3 disabled:opacity-50 disabled:cursor-not-allowed hover:cursor-pointer"
            aria-label="Produit suivant"
            @click="nextSlide"
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
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- About Us -->
    <section>
      <h2 class="text-3xl font-heading text-center mb-4">Qui sommes nous ?</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 items-center">
        <div
          class="h-40 lg:h-64 rounded-xl border-2 border-dark-purple bg-grey-purple flex items-center justify-center"
        >
          Image à venir
        </div>
        <div>
          <p class="text-lg text-justify mx-2">
            Mamie pull incarne l’image chaleureuse et confortable d’une mère
            tricotant des pulls depuis 1980. Elle symbolise la douceur, la
            patience et l’amour familial. Mamie Pull est souvent représentée
            assise dans un fauteuil moelleux avec une couverture sur les épaules
            et une tasse de thé bien chaude. Elle est entourée de pelotes de
            laine colorées et de deux chats ronronnant à ses peids. Mamie Pull
            est un exemple de sagesse et de bienveillance, transmettant non
            seulement son savoir-faire en tricot, mais aussi des valeurs de
            paratge et de générosité. A travers ses créations, réchuffant non
            seulement les corps mais aussi les coeurs.
          </p>
        </div>
      </div>
    </section>

    <!-- Category Buttons -->
    <section>
      <h2 class="text-3xl font-heading text-center mb-4">
        Explorer par catégorie
      </h2>

      <div v-if="catLoading" class="text-center py-10 text-light-purple">
        Chargement des catégories...
      </div>
      <div v-else-if="catError" class="text-center py-10 text-error-purple">
        Erreur : {{ catError }}
      </div>
      <div
        v-else-if="categories.length === 0"
        class="text-center py-10 text-light-purple"
      >
        Pas de catégories disponibles.
      </div>

      <div v-else class="flex flex-col sm:flex-row flex-wrap gap-3">
        <ButtonDark
          v-for="category in categories"
          :key="category.id"
          class="w-full sm:w-auto px-6 py-3 rounded-full transition text-lg"
          button-type="button"
          @click="goToCategory(category.slug)"
        >
          {{ category.name }}
        </ButtonDark>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCategoryStore } from '../stores/categoryStore'
import { getAllProducts } from '../api/products'
import ButtonDark from '../components/ButtonDark.vue'

const router = useRouter()
const products = ref([])
const loading = ref(false)
const error = ref(null)
const currentSlide = ref(0)

const categoryStore = useCategoryStore()
const categories = categoryStore.categories
const catLoading = categoryStore.loading
const catError = categoryStore.error

const fetchLatestProducts = async () => {
  loading.value = true
  error.value = null

  try {
    const data = await getAllProducts()
    products.value = data ?? []
  } catch (e) {
    error.value = e.message || 'Impossible de charger les produits.'
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  await categoryStore.fetchCategories()
}

onMounted(async () => {
  await Promise.all([fetchLatestProducts(), fetchCategories()])
})

const latestProducts = computed(() => products.value.slice(0, 4))

const goToCategory = (slug) => {
  if (!slug) return
  router.push({ name: 'category', params: { slug } })
}

const previousSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  }
}

const nextSlide = () => {
  if (currentSlide.value < latestProducts.value.slice(0, 3).length - 1) {
    currentSlide.value++
  }
}

const goToSlide = (index) => {
  currentSlide.value = index
}
</script>
