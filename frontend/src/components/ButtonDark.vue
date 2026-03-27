<template>
    <button class="bg-dark-purple-700 hover:cursor-pointer 
        text-white-purple-100 py-2 px-4 rounded-lg mx-auto 
        sg:w-30 lg:w-40" type="submit">{{ buttonText }}</button>
</template>

<script setup>
    defineProps(['buttonText'])
</script>