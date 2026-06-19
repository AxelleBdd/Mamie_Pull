<template>
  <div
    id="app"
    class="min-h-screen flex flex-col font-body bg-white-purple text-dark-purple"
  >
    <header class="bg-white-purple shadow-sm border-b border-grey-purple">
      <div class="max-w-7xl mx-auto px-6 py-2">
        <div class="flex items-center justify-between gap-8">
          <div class="shrink-0">
            <router-link to="/" aria-label="Accueil">
              <img
                src="./assets/Logos/Logo-rectangle.png"
                alt="Logo MamiePull"
                class="h-12 md:h-16 w-auto"
              />
            </router-link>
          </div>

          <!-- Desktop Navigation -->
          <nav
            class="hidden md:flex items-center gap-6 flex-1 ml-10"
            aria-label="Navigation principale"
          >
            <router-link
              to="/"
              class="px-4 py-2 rounded-md text-xl hover:bg-grey-purple transition"
            >
              Accueil
            </router-link>

            <!-- Products dropdown -->
            <div
              class="relative"
              @focusout="closeDropdownMenu('products', $event)"
            >
              <button
                class="flex items-center gap-1 px-4 py-2 rounded-md text-xl hover:bg-grey-purple transition"
                :aria-expanded="menus.products.value"
                aria-haspopup="true"
                @click="menus.products.value = !menus.products.value"
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
                v-show="menus.products.value"
                class="absolute left-0 w-64 bg-white border border-grey-purple rounded-md shadow-lg z-50 py-2 font-normal"
                role="menu"
              >
                <router-link
                  to="/products"
                  class="block px-4 py-2 hover:bg-white-purple transition"
                  role="menuitem"
                >
                  Tous nos produits
                </router-link>
                <hr class="my-1 border-grey-purple" />
                <router-link
                  v-for="category in validCategories"
                  :key="category.id"
                  :to="`/categories/${category.slug}`"
                  class="block px-4 py-2 hover:bg-white-purple transition"
                  role="menuitem"
                >
                  {{ category.name }}
                </router-link>
              </div>
            </div>
          </nav>

          <!-- Account dropdown -->
          <div class="hidden md:flex items-center gap-4">
            <div
              class="relative"
              @focusout="closeDropdownMenu('account', $event)"
            >
              <button
                class="flex items-center gap-2 p-2 hover:bg-grey-purple rounded-md transition"
                :aria-expanded="menus.account.value"
                aria-haspopup="true"
                @click="menus.account.value = !menus.account.value"
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
                v-show="menus.account.value"
                class="absolute right-0 w-48 bg-white border border-grey-purple rounded-md shadow-lg z-50 py-2"
                role="menu"
              >
                <template v-if="isAuthenticated">
                  <router-link
                    to="/profile"
                    class="block px-4 py-2 hover:bg-white-purple"
                    role="menuitem"
                  >
                    Mon profil
                  </router-link>
                  <router-link
                    to="/favorites"
                    class="block px-4 py-2 hover:bg-white-purple"
                    role="menuitem"
                  >
                    Mes favoris
                  </router-link>
                  <router-link
                    v-if="isStaff"
                    to="/admin/products"
                    class="block px-4 py-2 hover:bg-white-purple"
                    role="menuitem"
                  >
                    Admin - Produits
                  </router-link>
                  <button
                    class="w-full text-left px-4 py-2 hover:bg-red-50"
                    role="menuitem"
                    @click="logout()"
                  >
                    Déconnexion
                  </button>
                </template>
                <template v-else>
                  <router-link
                    to="/login"
                    class="block px-4 py-2 hover:bg-white-purple text-highlight-purple font-bold"
                    role="menuitem"
                  >
                    Connexion
                  </router-link>
                  <router-link
                    to="/register"
                    class="block px-4 py-2 hover:bg-white-purple text-highlight-purple font-bold"
                    role="menuitem"
                  >
                    S'inscrire
                  </router-link>
                </template>
              </div>
            </div>
          </div>

          <!-- Mobile menu toggle -->
          <button
            class="md:hidden p-2 rounded-md hover:bg-grey-purple transition"
            :aria-expanded="mobileMenu"
            aria-controls="mobile-menu"
            @click="mobileMenu = !mobileMenu"
          >
            <svg
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenu"
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
          v-if="mobileMenu"
          id="mobile-menu"
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
                @click="mobileMenu = false"
              >
                Accueil
              </router-link>
            </li>
            <li>
              <router-link
                to="/products"
                class="block px-4 py-2 rounded-md text-base"
                @click="mobileMenu = false"
              >
                Tous nos produits
              </router-link>
            </li>
            <li v-for="category in validCategories" :key="category.id">
              <router-link
                v-if="category.slug"
                :to="`/categories/${category.slug}`"
                class="block px-4 py-2 pl-10 rounded-md text-base hover:bg-grey-purple"
                @click="mobileMenu = false"
              >
                {{ category.name }}
              </router-link>
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
                  @click="mobileMenu = false"
                >
                  Mon profil
                </router-link>
              </li>
              <li>
                <router-link
                  to="/favorites"
                  class="block px-4 py-2 rounded-md text-base"
                  @click="mobileMenu = false"
                >
                  Mes favoris
                </router-link>
              </li>
              <li>
                <button
                  class="w-full text-left px-4 py-2"
                  @click="logoutAndClose"
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
                  @click="mobileMenu = false"
                >
                  Connexion
                </router-link>
              </li>
              <li>
                <router-link
                  to="/register"
                  class="block px-4 py-2 rounded-md text-base"
                  @click="mobileMenu = false"
                >
                  S'inscrire
                </router-link>
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
import { useRoute, useRouter } from 'vue-router'
import { useCategoryStore } from './stores/categoryStore'
import { useAuthStore } from './stores/authStore'
import { useSearchStore } from './stores/searchStore'
import { storeToRefs } from 'pinia'

const mobileMenu = ref(false)
const productsMenu = ref(false)
const accountMenu = ref(false)

const menus = {
  products: productsMenu,
  account: accountMenu,
}

const route = useRoute()
const router = useRouter()
const categoryStore = useCategoryStore()
const searchStore = useSearchStore()
const authStore = useAuthStore()
const { isAuthenticated, isStaff } = storeToRefs(authStore)

const displayFirstName = computed(() => {
  if (!authStore.user) return null
  return authStore.user.first_name || null
})

const validCategories = computed(() => {
  return categoryStore.categories.filter((cat) => cat && cat.slug)
})

const logout = () => {
  authStore.logout()
  router.push('/')
}

const logoutAndClose = () => {
  logout()
  mobileMenu.value = false
}

// Close a dropdown only if focus has truly left the container
const closeDropdownMenu = (menuName, event) => {
  const container = event.currentTarget
  setTimeout(() => {
    if (!container.contains(document.activeElement)) {
      menus[menuName].value = false
    }
  }, 150)
}

// Close all dropdowns on Escape
const handleEscape = (e) => {
  if (e.key === 'Escape') {
    Object.values(menus).forEach((menu) => {
      menu.value = false
    })
  }
}

onMounted(() => {
  categoryStore.fetchCategories()
  authStore.restoreSession()
  document.addEventListener('keydown', handleEscape)
})
</script>
