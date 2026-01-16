<template>
  <div id="app" class="min-h-screen flex flex-col font-body bg-[var(--color-white-purple-100)] text-[var(--color-dark-purple-700)]">
    
    <!-- Navbar -->
    <nav class="bg-white shadow-sm">
      <div
        class="max-w-7xl mx-auto px-6 py-4 flex flex-col gap-4
               md:flex-row md:items-center md:justify-between"
      >
        <!-- Logo TODO: Change logo-->
        <router-link
          to="/"
          class="font-heading text-2xl md:text-3xl text-[var(--color-highlight-purple-500)] hover:opacity-80 transition"
        >
          🧶 MamiePull
        </router-link>

        <!-- Menu TODO: Change menus when on smaller screens -->
        <ul class="flex gap-4 md:gap-6">
          <li>
            <router-link
              to="/"
              class="px-4 py-2 rounded-md text-sm md:text-base
                     hover:bg-[var(--color-grey-purple-400)]
                     transition"
            >
              Accueil
            </router-link>
          </li>
          <li>
            <router-link
              to="/products"
              class="px-4 py-2 rounded-md text-sm md:text-base
                     hover:bg-[var(--color-grey-purple-400)]
                     transition"
            >
              Catalogue
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main -->
    <main class="flex-1 py-8 md:py-12">
      <router-view />
    </main>

    <!-- Footer TODO: Change footer to match design -->
    <footer class="bg-white border-t">
      <div
        class="max-w-7xl mx-auto px-6 py-6 text-center text-sm md:text-base"
      >
        <p>
          &copy; 2025 MamiePull – Produits faits main avec amour 💜
        </p>
      </div>
    </footer>

  </div>
</template>

<script setup>
</script>
