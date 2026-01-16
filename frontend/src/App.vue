<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <router-link to="/" class="logo">
          🧶 MamiePull
        </router-link>
        
        <ul class="nav-menu">
          <li>
            <router-link to="/" class="nav-link">
              Accueil
            </router-link>
          </li>
          <li>
            <router-link to="/products" class="nav-link">
              Catalogue
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="footer">
      <div class="footer-container">
        <p>&copy; 2025 MamiePull - Produits faits main avec amour</p>
      </div>
    </footer>
  </div>
</template>

<script setup>

</script>

<style>
/* General Styles */

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
    flex-direction: column;
    gap: 1rem;
  }

  .nav-menu {
    gap: 1rem;
  }

  .nav-link {
    font-size: 0.9rem;
    padding: 0.4rem 0.8rem;
  }

  .logo {
    font-size: 1.25rem;
  }

  .main-content {
    padding: 1rem 0;
  }

  .footer-container {
    padding: 1.5rem 1rem;
  }

  .footer p {
    font-size: 0.875rem;
  }
}
</style>