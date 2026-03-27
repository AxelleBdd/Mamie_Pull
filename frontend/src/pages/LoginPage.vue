<template>
    <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <h2 class="mt-10 text-center text-4xl sm:text-5xl lg:text-6xl font-bold font-heading tracking-tight"><u>Connexion</u></h2>
        </div>

        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm bg-grey-purple-400 rounded-lg space-y-10 p-10">
        <form class="space-y-6" @submit.prevent>
            <div>
                <label for="email" class="block font-heading text-3xl font-medium">Email</label>
                <div class="mt-2">
                    <input type="email" v-model="email" name="email" id="email" autocomplete="email" placeholder="example@email.com" required 
                    class="block w-full bg-white-purple-100 rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple-700 focus:outline-2" />
                </div>
            </div>

            <div>
                <div class="flex items-center justify-between">
                    <label for="password" class="block font-heading text-3xl">Mot de passe</label>
                    <div class="text-sm">
                        <!-- TODO: <a href="#" class="font-semibold text-highlight-purple-500">Forgot password?</a> -->
                    </div>
                </div>
                <div class="mt-2 relative">
                    <input :type="isVisible ? 'text' : 'password'" v-model="password" name="password" id="password" placeholder="Entrez votre mot de passe..." required 
                    class="block w-full bg-white-purple-100 rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple-700 focus:outline-2" />
                    <button type="button" @click="toggleVisibility"
                        :aria-label="isVisible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
                        :aria-pressed="isVisible.toString()" aria-controls="password"
                        class="absolute inset-y-0 right-2 flex items-center">

                        <svg v-if="!isVisible" class="h-5 w-5 text-dark-purple-700 cursor-pointer"
                            fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M2.458 12C3.732 7.943 7.523 5 12 5
                                c4.477 0 8.268 2.943 9.542 7
                                -1.274 4.057-5.065 7-9.542 7
                                -4.477 0-8.268-2.943-9.542-7z" />
                        </svg>

                        <svg v-else class="h-5 w-5 text-dark-purple-700 cursor-pointer" fill="none"
                            viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M3 3l18 18M9.88 9.88
                                a3 3 0 104.24 4.24M6.18 6.18
                                A9.956 9.956 0 0112 5
                                c4.477 0 8.268 2.943
                                9.542 7a9.97 9.97 0 01-4.043 5.132" />
                        </svg>
                    </button>
                </div>
            </div>

            <div class="flex gap-4 mt-12">
                <ButtonLight buttonText="Créer un compte" link="/register"/>
                <ButtonDark buttonText="Se connecter" @click="login"/>
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

    // Form data
    const email = ref('')
    const password = ref('')
    const isVisible = ref(false)
    const error = ref(null)

    const toggleVisibility = () => {
    isVisible.value = !isVisible.value
    }

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