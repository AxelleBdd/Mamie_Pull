<template>
    <div class="max-w-400 mx-auto px-4 md:px-8 lg:px-12 py-4">
    <!-- Header -->
        <header class="text-center my-4">
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading"><u>Connexion</u></h1>
        </header>
    </div>

    <form class="my-8 max-w-sm lg:max-w-md mx-auto bg-grey-purple-400 p-5 rounded-lg space-y-10 p-10" action="login">
        <div id="email">
            <label class="font-heading text-3xl block" for="email">Email</label>
            <input class="block border border-dark-purple-700 bg-white-purple-100 rounded-lg p-2 w-70 mx-auto mt-4" 
            type="email" id="email" name="email" placeholder="example@email.com" required>
        </div>
        <div id="password" class="mt-10">
            <label class="font-heading text-3xl block" for="password">Mot de passe</label>
            <div class="relative w-70 mx-auto mt-4">
                <input :type="isVisible ? 'text' : 'password'" v-model="password" id="password"
                    name="password" class="block border border-dark-purple-700 bg-white-purple-100 rounded-lg p-2 w-full pr-10"
                    placeholder="Entrez votre mot de passe..."  required />
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
            <p v-if="error" class="text-error-purple-900 flex mt-4">
                <svg fill="#5E1E22" height="20px" width="20px"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 57.602 57.602">
                    <path d="M57.337,52.327L30.353,3.279c-0.361-0.617-1.005-0.986-1.722-0.986c-0.721,0-1.366,
                        0.373-1.74,1.02L0.272,52.313c-0.362,0.624-0.363,1.371-0.002,1.997c0.36,0.625,1.007,0.999,
                        1.729,0.999h53.603c0.724,0,1.371-0.375,1.731-1.003C57.693,53.678,57.689,52.93,57.337,52.327z
                        M5.539,51.309L28.642,8.15l23.396,43.159H5.539z"/>
                    <path d="M27.599,21.309v17c0,0.553,0.447,1,1,1s1-0.447,1-1v-17c0-0.553-0.447-1-1-1S27.599,
                        20.757,27.599,21.309z"/>
                    <path d="M28.599,41.309c-0.553,0-1,0.447-1,1v2c0,0.553,0.447,1,1,1s1-0.447,1-1v-2C29.599,
                        41.757,29.151,41.309,28.599,41.309z"/>
                </svg>
                <span class="ml-2">{{ error }}</span>
            </p>
        </div>
        <div class="flex space-x-5 mt-12">
            <ButtonLight buttonText="Créer un compte"/>
            <ButtonDark buttonText="Se connecter" @click="login"/>
        </div>
    </form>
</template>

<script setup>
    import { ref, onMounted } from 'vue'
    import { useSessionStore } from '../stores/sessionStore'
    import { storeToRefs } from 'pinia'

    import ButtonDark from '../components/ButtonDark.vue'
    import ButtonLight from '../components/ButtonLight.vue'

    // Visibility of the password input
    const username = ref('')
    const password = ref('')
    const isVisible = ref(false)

    const toggleVisibility = () => {
    isVisible.value = !isVisible.value
    }
    //Error message
    const error = ref(null)

    const store = useSessionStore()
    const { isLoggedIn, user } = storeToRefs(store)

    const login = async () => {
    error.value = null
    const success = await store.login(username.value, password.value)
    if (!success) error.value = 'Email ou mot de passe incorrect'
    }

    const logout = () => {
    store.logout()
    }

    onMounted(() => {
    store.loadSession()
    })

    // Send connection request to the backend
    // const handleSubmit = async () => {
    //     try {
    //         const response = await fetch('/api/login', {
    //             method: 'POST',
    //             headers: {
    //                 'Content-Type': 'application/json'
    //             },
    //             body: JSON.stringify({ email: email.value, password: password.value })
    //         })
    //     } catch(error) {
    //         console.error('Error during login:', error)
    //     }
    // }
</script>