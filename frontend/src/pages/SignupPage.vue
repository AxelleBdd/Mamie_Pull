<template>
  <div
    class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8"
  >
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2
        class="mt-10 text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight"
      >
        <u>Créer mon compte</u>
      </h2>
    </div>

    <div
      class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm md:max-w-md bg-grey-purple rounded-lg space-y-10 p-10"
    >
      <form class="space-y-6" @submit.prevent="signup">
        <div>
          <label for="last_name" class="block font-heading text-3xl font-medium"
            >Nom de famille</label
          >
          <div class="mt-2">
            <input
              id="last_name"
              v-model="last_name"
              type="text"
              name="last_name"
              autocomplete="family-name"
              placeholder="Dupont"
              required
              class="block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple focus:outline-2"
            />
          </div>
        </div>
        <div>
          <label
            for="first_name"
            class="block font-heading text-3xl font-medium"
            >Prénom</label
          >
          <div class="mt-2">
            <input
              id="first_name"
              v-model="first_name"
              type="text"
              name="first_name"
              autocomplete="given-name"
              placeholder="Léa"
              required
              class="block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple focus:outline-2"
            />
          </div>
        </div>
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

        <PasswordInput
          id="password"
          v-model="password"
          name="password"
          placeholder="Entrez votre mot de passe..."
        />
        <PasswordInput
          id="confirm_password"
          v-model="confirm_password"
          label="Confirmer le mot de passe"
          name="confirm_password"
          autocomplete="new-password"
          placeholder="Confirmez votre mot de passe..."
        />

        <div
          v-if="error"
          class="text-error-purple px-4 py-3 rounded mb-4"
          role="alert"
        >
          <span class="block sm:inline">{{ error }}</span>
        </div>
        <div class="flex gap-4 mt-12">
          <router-link
            to="/login"
            class="bg-white-purple hover:cursor-pointer hover:bg-white text-dark-purple py-2 px-4 rounded-lg mx-auto sg:w-30 lg:w-40"
          >
            J'ai déjà un compte
          </router-link>
          <ButtonDark type="submit" button-text="Créer mon compte" />
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
import ButtonLight from '../components/ButtonLight.vue'
import PasswordInput from '../components/PasswordInput.vue'

// Form data
const last_name = ref('')
const first_name = ref('')
const email = ref('')
const password = ref('')
const confirm_password = ref('')
const isVisible = ref(false)
const error = ref(null)

const toggleVisibility = () => {
  isVisible.value = !isVisible.value
}

const store = useAuthStore()
const router = useRouter()

const signup = async () => {
  error.value = null
  try {
    await store.signup({
      username: email.value,
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
      password_confirm: confirm_password.value,
    })
    router.push('/')
  } catch (err) {
    // Message from authService if the backends returns an error
    error.value =
      err.message || 'Une erreur est survenue lors de la création du compte.'
  }
}
</script>
