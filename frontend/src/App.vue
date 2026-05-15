<template>
  <div
    id="app"
    class="min-h-screen flex flex-col font-body bg-white-purple text-dark-purple"
  >
    <header class="bg-white-purple shadow-sm border-b border-grey-purple">
      <div class="max-w-7xl mx-auto px-6 py-2">
        <div class="flex items-center justify-between gap-8">
          <div class="shrink-0">
            <router-link to="/">
              <img
                src="./assets/Logos/Logo-rectangle.png"
                alt="Logo MamiePull"
                class="h-12 md:h-16 w-auto"
              />
            </router-link>
          </div>

          <!-- Desktop Navigation -->
          <nav class="hidden md:flex items-center gap-6 flex-1 ml-10">
            <router-link
              to="/"
              class="px-4 py-2 rounded-md text-xl hover:bg-grey-purple transition"
            >
              Accueil
            </router-link>

            <div class="relative group">
              <button
                class="flex items-center gap-1 px-4 py-2 rounded-md text-xl hover:bg-grey-purple transition"
              >
                Nos produits
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M19 9l-7 7-7-7"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
              <div
                class="absolute left-0 w-64 bg-white border border-grey-purple rounded-md shadow-lg hidden group-hover:block z-50 py-2 font-normal"
              >
                <router-link
                  to="/products"
                  class="block px-4 py-2 hover:bg-white-purple transition"
                >
                  Tous nos produits
                </router-link>
                <hr class="my-1 border-grey-purple" />
                <router-link
                  v-for="category in validCategories"
                  :key="category.id"
                  :to="`/categories/${category.slug}`"
                  class="block px-4 py-2 hover:bg-white-purple transition"
                >
                  {{ category.name }}
                </router-link>
              </div>
            </div>
          </nav>

          <div class="hidden md:flex items-center gap-4">
            <router-link
              v-if="isAuthenticated"
              to="/favoris"
              class="p-2 hover:bg-grey-purple rounded-full transition"
              title="Favoris"
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
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                />
              </svg>
            </router-link>

            <div class="relative group">
              <button
                class="flex items-center gap-2 p-2 hover:bg-grey-purple rounded-md transition"
              >
                <svg
                  class="w-7 h-7"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
                <span
                  v-if="isAuthenticated && displayFirstName"
                  class="text-lg"
                >
                  {{ displayFirstName }}
                </span>
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M19 9l-7 7-7-7"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
              <div
                class="absolute right-0 w-48 bg-white border border-grey-purple rounded-md shadow-lg hidden group-hover:block z-50 py-2"
              >
                <template v-if="isAuthenticated">
                  <router-link
                    to="/profile"
                    class="block px-4 py-2 hover:bg-white-purple"
                    >Mon profil</router-link
                  >
                  <router-link
                    v-if="isStaff"
                    to="/admin/products"
                    class="block px-4 py-2 hover:bg-white-purple"
                    >Admin - Produits</router-link
                  >
                  <button
                    class="w-full text-left px-4 py-2 hover:bg-red-50"
                    @click="logout()"
                  >
                    Déconnexion
                  </button>
                </template>
                <template v-else>
                  <router-link
                    to="/login"
                    class="block px-4 py-2 hover:bg-white-purple text-highlight-purple font-bold"
                    >Connexion</router-link
                  >
                  <router-link
                    to="/register"
                    class="block px-4 py-2 hover:bg-white-purple text-highlight-purple font-bold"
                    >S'inscrire</router-link
                  >
                </template>
              </div>
            </div>
          </div>

          <button
            class="md:hidden p-2 rounded-md hover:bg-grey-purple transition"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <!-- Mobile Menu -->
        <div
          v-if="mobileMenuOpen"
          class="md:hidden mt-4 pt-4 border-t border-grey-purple"
        >
          <p
            class="text-lg font-semibold text-dark-purple mb-2 px-4 italic underline"
          >
            Navigation
          </p>
          <ul class="flex flex-col gap-1 mb-4">
            <li>
              <router-link
                to="/"
                class="block px-4 py-2 rounded-md text-base"
                @click="mobileMenuOpen = false"
                >Accueil</router-link
              >
            </li>
            <li>
              <router-link
                to="/products"
                class="block px-4 py-2 rounded-md text-base"
                @click="mobileMenuOpen = false"
                >Tous nos produits</router-link
              >
            </li>
            <li v-for="category in validCategories" :key="category.id">
              <router-link
                v-if="category.slug"
                :to="`/categories/${category.slug}`"
                class="block px-4 py-2 pl-10 rounded-md text-base hover:bg-grey-purple"
                @click="mobileMenuOpen = false"
                >{{ category.name }}</router-link
              >
            </li>
          </ul>

          <p
            class="text-lg font-semibold text-dark-purple mb-2 px-4 italic underline"
          >
            Compte
          </p>
          <ul class="flex flex-col gap-1 pb-4">
            <template v-if="isAuthenticated">
              <li>
                <router-link
                  to="/profile"
                  class="block px-4 py-2 rounded-md text-base"
                  @click="mobileMenuOpen = false"
                  >Mon profil</router-link
                >
              </li>
              <li>
                <router-link
                  to="/favoris"
                  class="block px-4 py-2 rounded-md text-base"
                  @click="mobileMenuOpen = false"
                  >Favoris</router-link
                >
              </li>
              <li>
                <button
                  class="w-full text-left px-4 py-2"
                  @click="
                    (logout(), // eslint-disable-line , necessary
                    (mobileMenuOpen = false))
                  "
                >
                  Déconnexion
                </button>
              </li>
            </template>
            <template v-else>
              <li>
                <router-link
                  to="/login"
                  class="block px-4 py-2 rounded-md text-base"
                  @click="mobileMenuOpen = false"
                  >Connexion</router-link
                >
              </li>
              <li>
                <router-link
                  to="/register"
                  class="block px-4 py-2 rounded-md text-base"
                  @click="mobileMenuOpen = false"
                  >S'inscrire</router-link
                >
              </li>
            </template>
          </ul>
        </div>
      </div>
    </header>

    <main class="flex-1 font-body">
      <router-view />
    </main>

    <footer class="bg-dark-purple border-t border-grey-purple">
      <div
        class="max-w-7xl mx-auto px-6 py-6 text-center text-white-purple text-sm md:text-base"
      >
        <p>2025 MamiePull &copy; – Produits faits main avec amour 💜</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCategoryStore } from './stores/categoryStore'
import { useAuthStore } from './stores/authStore'
import { useSearchStore } from './stores/searchStore'
import { storeToRefs } from 'pinia'

const mobileMenuOpen = ref(false)
const route = useRoute()
const categoryStore = useCategoryStore()
const searchStore = useSearchStore()

// User session management
const authStore = useAuthStore()
const { isAuthenticated, isStaff } = storeToRefs(authStore)

// Display user name in the header
const displayFirstName = computed(() => {
  if (!authStore.user) return null
  const first_name = authStore.user.first_name
  return first_name || null
})

// Display categories in the navigation
const validCategories = computed(() => {
  return categoryStore.categories.filter((cat) => cat && cat.slug)
})

const logout = () => {
  authStore.logout()
}

onMounted(() => {
  categoryStore.fetchCategories()
  authStore.restoreSession()
})
</script>
