<template>
    <div class="max-w-400 mx-auto px-4 md:px-8 lg:px-12 py-4">
    <!-- Header -->
        <header class="text-center my-4">
            <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold font-heading"><u>Connexion</u></h1>
        </header>
    </div>

    <form class="mt-8 max-w-md mx-auto" action="login">
        <div id="email">
            <label class="font-heading text-3xl block" for="email">Email</label>
            <input class="block border border-dark-purple-700 bg-white rounded-lg p-2 w-70 mx-auto mt-4 mb-8 text-center" 
            type="email" id="email" name="email" placeholder="example@email.com" required>
        </div>
        <div id="password">
            <label class="font-heading text-3xl block" for="password">Mot de passe</label>
            <input class="block border border-dark-purple-700 bg-white rounded-lg p-2  mx-auto my-4 w-70 text-center" 
            type="password" id="password" name="password" placeholder="Entrez votre mot de passe..." required>
        </div>
</form>

</template>