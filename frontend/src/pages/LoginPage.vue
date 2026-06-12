<template>
  <div
    class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8"
  >
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2
        class="mt-10 text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight"
      >
        <u>Connexion</u>
      </h2>
    </div>

    <div
      class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm bg-grey-purple rounded-lg space-y-10 p-10"
    >
      <form class="space-y-6" @submit.prevent="login">
        <div>
          <label for="email" class="block font-heading text-3xl font-medium"
            >Email</label
          >
          <div class="mt-2">
            <input
              id="email"
              v-model="email"
              type="email"
              name="email"
              autocomplete="email"
              placeholder="example@email.com"
              required
              class="block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple focus:outline-2"
            />
          </div>
        </div>

        <div>
          <PasswordInput
            id="password"
            v-model="password"
            :validate="false"
            autocomplete="current-password"
            placeholder="Entrez votre mot de passe..."
          />
          <p v-if="error" role="alert" class="mt-1 text-sm text-error-purple">
            {{ error }}
          </p>
        </div>

        <div class="flex gap-4 mt-12">
          <router-link
            to="/register"
            class="bg-white-purple hover:cursor-pointer hover:bg-white text-dark-purple py-2 px-4 rounded-lg mx-auto sg:w-30 lg:w-40"
          >
            Créer un compte
          </router-link>
          <ButtonDark type="submit" button-text="Se connecter" />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import ButtonDark from '../components/ButtonDark.vue'
import PasswordInput from '../components/PasswordInput.vue'

// Form data
const email = ref('')
const password = ref('')
const error = ref(null)

const store = useAuthStore()
const router = useRouter()

const login = async () => {
  error.value = null
  try {
    await store.login(email.value, password.value)
    router.push('/')
  } catch (err) {
    // Message from authService if the backends returns an error
    error.value = err.message || 'Email ou mot de passe incorrect'
  }
}
</script>
