<template>
  <div
    class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8"
  >
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
      <h2
        class="mt-10 text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight"
      >
        <u>Mon Profil</u>
      </h2>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !user" class="sm:mx-auto sm:w-full sm:max-w-sm mt-10">
      <div class="text-center py-10">
        <div
          class="mx-auto mb-4 h-12 w-12 rounded-full border-4 border-highlight-purple animate-spin"
        ></div>
        <p class="text-base text-light-purple">Chargement du profil...</p>
      </div>
    </div>

    <!-- Error State -->
    <div
      v-else-if="error && !user"
      class="sm:mx-auto sm:w-full sm:max-w-sm mt-10"
    >
      <div class="text-center py-10">
        <p class="text-error-purple font-semibold mb-4">{{ error }}</p>
        <router-link
          to="/"
          class="bg-white-purple hover:bg-grey-purple text-dark-purple py-2 px-4 rounded-lg transition"
        >
          Retour à l'accueil
        </router-link>
      </div>
    </div>

    <!-- Profile Form -->
    <div
      v-else-if="user"
      class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm md:max-w-md bg-grey-purple rounded-lg space-y-10 p-10"
    >
      <!-- Success Message -->
      <div
        v-if="successMessage"
        class="text-highlight-purple bg-white-purple px-4 py-3 rounded mb-4"
        role="alert"
      >
        <span class="block sm:inline">{{ successMessage }}</span>
      </div>

      <!-- Error Message -->
      <div
        v-if="errorMessage"
        class="text-error-purple px-4 py-3 rounded mb-4"
        role="alert"
      >
        <span class="block sm:inline">{{ errorMessage }}</span>
      </div>

      <form class="space-y-6" @submit.prevent>
        <!-- First Name -->
        <div>
          <label
            for="first_name"
            class="block font-heading text-3xl font-medium"
            >Prénom</label
          >
          <div class="mt-2">
            <input
              id="first_name"
              v-model="formData.first_name"
              type="text"
              name="first_name"
              autocomplete="given-name"
              placeholder="Léa"
              class="block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple focus:outline-2"
            />
          </div>
        </div>

        <!-- Last Name -->
        <div>
          <label for="last_name" class="block font-heading text-3xl font-medium"
            >Nom de famille</label
          >
          <div class="mt-2">
            <input
              id="last_name"
              v-model="formData.last_name"
              type="text"
              name="last_name"
              autocomplete="family-name"
              placeholder="Dupont"
              class="block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple focus:outline-2"
            />
          </div>
        </div>

        <!-- Email -->
        <div>
          <label for="email" class="block font-heading text-3xl font-medium"
            >Email</label
          >
          <div class="mt-2">
            <input
              id="email"
              v-model="formData.email"
              type="email"
              name="email"
              autocomplete="email"
              placeholder="example@email.com"
              class="block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple focus:outline-2"
            />
          </div>
        </div>

        <!-- Actions -->
        <div class="flex gap-3 mt-12">
          <router-link
            to="/"
            class="bg-white-purple text-dark-purple py-2 px-4 rounded-lg mx-auto sg:w-30 lg:w-40 text-center place-content-center"
          >
            Annuler
          </router-link>
          <ButtonDark
            button-text="Enregistrer les modifications"
            :disabled="updating"
            @click="updateProfile"
          />
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '../stores/authStore'
import { getCurrentUser, updateUser } from '../api/users'
import ButtonDark from '../components/ButtonDark.vue'

const router = useRouter()
const authStore = useAuthStore()
const { accessToken } = storeToRefs(authStore)

const user = ref(null)
const loading = ref(false)
const updating = ref(false)
const error = ref(null)
const errorMessage = ref(null)
const successMessage = ref(null)

const formData = reactive({
  first_name: '',
  last_name: '',
  email: '',
})

const fetchUserProfile = async () => {
  loading.value = true
  error.value = null

  try {
    if (!accessToken.value) {
      throw new Error('Vous devez être connecté pour voir votre profil')
    }

    const userData = await getCurrentUser(accessToken.value)
    user.value = userData
    Object.assign(formData, userData)
  } catch (err) {
    error.value = err.message || 'Impossible de charger le profil'
  } finally {
    loading.value = false
  }
}

const updateProfile = async () => {
  errorMessage.value = null
  successMessage.value = null
  updating.value = true

  try {
    const updatedUser = await updateUser(accessToken.value, formData)
    user.value = updatedUser
    authStore.setUser(updatedUser)
    successMessage.value = 'Profil mis à jour avec succès !'
    setTimeout(() => {
      successMessage.value = null
    }, 3000)
  } catch (err) {
    errorMessage.value = err.message || 'Impossible de mettre à jour le profil'
  } finally {
    updating.value = false
  }
}

const logout = async () => {
  authStore.logout()
  await router.push('/login')
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
  } else {
    fetchUserProfile()
  }
})
</script>
