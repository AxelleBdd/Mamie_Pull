<template>
  <div
    id="app"
    class="min-h-screen flex flex-col font-body bg-white-purple-100 text-dark-purple-700"
  >
    <header
      class="bg-white-purple-100 shadow-sm border-b border-grey-purple-300"
    >
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
              class="px-4 py-2 rounded-md text-xl hover:bg-grey-purple-400 transition"
            >
              Accueil
            </router-link>

            <div class="relative group">
              <button
                class="flex items-center gap-1 px-4 py-2 rounded-md text-xl hover:bg-grey-purple-400 transition"
              >
                Nos Produits
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
                class="absolute left-0 w-64 bg-white border border-grey-purple-300 rounded-md shadow-lg hidden group-hover:block z-50 py-2 font-normal"
              >
                <router-link
                  to="/products"
                  class="block px-4 py-2 hover:bg-white-purple-100 transition"
                >
                  Tous nos produits
                </router-link>
                <hr class="my-1 border-grey-purple-400">
                <router-link
                  v-for="category in validCategories"
                  :key="category.id"
                  :to="`/categories/${category.slug}`"
                  class="block px-4 py-2 hover:bg-white-purple-100 transition"
                >
                  {{ category.name }}
                </router-link>
              </div>
            </div>
          </nav>

          <div class="hidden md:flex items-center gap-4">
            <router-link v-if="isAuthenticated" to="/favoris" class="p-2 hover:bg-grey-purple-400 rounded-full transition" title="Favoris">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
            </router-link>

            <div class="relative group">
              <button
                class="flex items-center gap-1 p-2 hover:bg-grey-purple-400 rounded-md transition"
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
              <div class="absolute right-0 w-48 bg-white border border-grey-purple-400 rounded-md shadow-lg hidden group-hover:block z-50 py-2">
                <template v-if="isAuthenticated">
                  <router-link to="/profil" class="block px-4 py-2 hover:bg-white-purple-100">Mon profil</router-link>
                  <button @click="logout()" class="w-full text-left px-4 py-2 hover:bg-red-50">Déconnexion</button>
                </template>
                <template v-else>
                  <router-link
                    to="/login"
                    class="block px-4 py-2 hover:bg-white-purple-100 text-highlight-purple-600 font-bold"
                    >Connexion</router-link
                  >
                  <router-link
                    to="/register"
                    class="block px-4 py-2 hover:bg-white-purple-100 text-highlight-purple-600 font-bold"
                    >S'inscrire</router-link
                  >
                </template>
              </div>
            </div>
          </div>

          <button
            class="md:hidden p-2 rounded-md hover:bg-grey-purple-400 transition"
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
          class="md:hidden mt-4 pt-4 border-t border-grey-purple-300"
        >
          <p
            class="text-lg font-semibold text-dark-purple-500 mb-2 px-4 italic underline"
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
                class="block px-4 py-2 pl-10 rounded-md text-base hover:bg-grey-purple-400"
                @click="mobileMenuOpen = false"
                >{{ category.name }}</router-link
              >
            </li>
          </ul>

          <p
            class="text-lg font-semibold text-dark-purple-500 mb-2 px-4 italic underline"
          >
            Compte
          </p>
          <ul class="flex flex-col gap-1 pb-4">
            <template v-if="isAuthenticated">
              <li><router-link to="/profil" class="block px-4 py-2 rounded-md text-base" @click="mobileMenuOpen = false">Mon profil</router-link></li>
              <li><router-link to="/favoris" class="block px-4 py-2 rounded-md text-base" @click="mobileMenuOpen = false">Favoris</router-link></li>
              <li><button @click="logout(); mobileMenuOpen = false" class="w-full text-left px-4 py-2">Déconnexion</button></li>
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

    <div v-if="showSearchBar" class="bg-white-purple-100">
      <div class="max-w-7xl mx-auto px-6 py-3">
        <div class="relative max-w-2xl mx-auto">
          <input
            type="search"
            placeholder="Rechercher un produit..."
            class="w-full px-4 py-2 pr-10 rounded-md border border-grey-purple-300 focus:outline-none focus:ring-2 focus:ring-highlight-purple-500 bg-white transition"
          />
          <svg
            class="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-dark-purple-500"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
            />
          </svg>
        </div>
      </div>
    </div>

    <main class="flex-1 font-body">
      <router-view />
    </main>

    <footer class="bg-dark-purple-700 border-t border-grey-purple-300">
      <div
        class="max-w-7xl mx-auto px-6 py-6 text-center text-white-purple-100 text-sm md:text-base"
      >
        <p>2025 MamiePull &copy; – Produits faits main avec amour 💜</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { useCategoryStore } from './stores/categoryStore'
  import { useAuthStore } from './stores/authStore'
  import { storeToRefs } from 'pinia'

const mobileMenuOpen = ref(false)
const route = useRoute()
const categoryStore = useCategoryStore()

  // User session management
  const authStore = useAuthStore()
  const { isAuthenticated } = storeToRefs(authStore)

  // Search bar visibility logic
  const showSearchBar = computed(() => {
    return route.path === '/' || route.path.startsWith('/products') || route.path.startsWith('/categories');
  });

  // Display categories in the navigation
  const validCategories = computed(() => {
  return categoryStore.categories.filter(cat => cat && cat.slug);
});

  const logout = () => {
    authStore.logout()
  }

  onMounted(() => {
    categoryStore.fetchCategories()
  })
</script>
