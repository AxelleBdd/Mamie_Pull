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
        </div>
        <div class="flex space-x-5 mt-12">
            <ButtonLight buttonText="Créer un compte" @click="createAccount"/>
            <ButtonDark buttonText="Se connecter" @click="handleSubmit"/>
        </div>
    </form>
</template>

<script setup>
    import { ref } from 'vue'
    import ButtonDark from '../components/ButtonDark.vue'
    import ButtonLight from '../components/ButtonLight.vue'

    // Visibility of the password input
    const password = ref('')
    const isVisible = ref(false)

    const toggleVisibility = () => {
    isVisible.value = !isVisible.value
    }

    // Send connection request to the backend
    const handleSubmit = async () => {
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email: email.value, password: password.value })
            })
        } catch(error) {
            console.error('Error during login:', error)
        }
    }
</script>