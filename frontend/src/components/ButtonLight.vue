<template>
    <button class="bg-white-purple-100 hover:cursor-pointer 
        text-dark-purple-700 py-2 px-4 rounded-lg mx-auto 
        sg:w-30 lg:w-40" type="submit">{{ buttonText }}</button>
</template>

<script setup>
    defineProps(['buttonText'])
</script>