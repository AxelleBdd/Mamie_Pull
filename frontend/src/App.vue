<template>
  <div id="app" class="min-h-screen flex flex-col font-body bg-white-purple-100 text-dark-purple-700">
    <header class="bg-white-purple-100 shadow-sm border-b border-grey-purple-300">
      <!-- Conteneur principal du header -->
      <div class="max-w-7xl mx-auto px-6 py-4">
        <!-- Logo + Navigation -->
        <div class="flex items-center justify-between gap-8">
          <!-- Logo -->
          <div class="flex-shrink-0">
            <img 
              src="./assets/Logos/Logo-rectangle.png" 
              alt="Logo MamiePull"
              class="h-12 md:h-16 w-auto"
            >
          </div>

          <!-- Navigation principale - Desktop -->
          <nav class="hidden md:flex items-center gap-2 flex-1 ml-8">
            <router-link
              to="/"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Accueil
            </router-link>
            <router-link
              to="/products"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Catalogue
            </router-link>
            <router-link
              to="/categories/pulls"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Pulls
            </router-link>
            <router-link
              to="/categories/echarpes"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Écharpes
            </router-link>
            <router-link
              to="/categories/bonnets"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Bonnets
            </router-link>
          </nav>

          <!-- Menu utilisateur - Desktop (aligné à droite) -->
          <div class="hidden md:flex items-center gap-2">
            <router-link
              to="/profil"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Mon Profil
            </router-link>
            <router-link
              to="/favoris"
              class="px-4 py-2 rounded-md text-base md:text-lg
                    hover:bg-grey-purple-400
                    transition"
            >
              Favoris
            </router-link>
          </div>

          <!-- Bouton menu burger - Mobile -->
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="md:hidden p-2 rounded-md hover:bg-grey-purple-400 transition"
            aria-label="Menu"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

        <!-- Menu mobile -->
        <div 
          v-if="mobileMenuOpen"
          class="md:hidden mt-4 pt-4 border-t border-grey-purple-300"
        >
          <!-- Navigation principale -->
          <div class="mb-4">
            <p class="text-sm font-semibold text-dark-purple-500 mb-2 px-4">Navigation</p>
            <ul class="flex flex-col gap-1">
              <li>
                <router-link
                  to="/"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Accueil
                </router-link>
              </li>
              <li>
                <router-link
                  to="/products"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Catalogue
                </router-link>
              </li>
              <li>
                <router-link
                  to="/categories/pulls"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Pulls
                </router-link>
              </li>
              <li>
                <router-link
                  to="/categories/echarpes"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Écharpes
                </router-link>
              </li>
              <li>
                <router-link
                  to="/categories/bonnets"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Bonnets
                </router-link>
              </li>
            </ul>
          </div>

          <!-- Navigation utilisateur -->
          <div>
            <p class="text-sm font-semibold text-dark-purple-500 mb-2 px-4">Mon compte</p>
            <ul class="flex flex-col gap-1">
              <li>
                <router-link
                  to="/profil"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Mon Profil
                </router-link>
              </li>
              <li>
                <router-link
                  to="/favoris"
                  class="block px-4 py-2 rounded-md text-base
                        hover:bg-grey-purple-400
                        transition"
                  @click="mobileMenuOpen = false"
                >
                  Favoris
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </header>

    <!-- Barre de recherche (conditionnelle selon la route) -->
    <div 
      v-if="showSearchBar"
      class="bg-white-purple-100"
    >
      <div class="max-w-7xl mx-auto px-6 py-3">
        <div class="relative max-w-2xl mx-auto">
          <input
            type="search"
            placeholder="Rechercher un produit..."
            class="w-full px-4 py-2 pr-10 rounded-md border border-grey-purple-300 
                   focus:outline-none focus:ring-2 focus:ring-[var(--color-highlight-purple-500)]
                   bg-white transition"
          >
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

    <!-- Main -->
    <main class="flex-1 py-8 md:py-12">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-white-purple-100 border-t border-grey-purple-300">
      <div class="max-w-7xl mx-auto px-6 py-6 text-center text-sm md:text-base">
        <p>&copy; 2025 MamiePull – Produits faits main avec amour 💜</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const mobileMenuOpen = ref(false);
const route = useRoute();

// Routes where the search bar should be displayed
const showSearchBar = computed(() => {
  return route.path === '/' || 
         route.path.startsWith('/products') || 
         route.path.startsWith('/categories');
});
</script>