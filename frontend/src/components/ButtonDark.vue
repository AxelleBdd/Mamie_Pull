<template>
  <button
    v-bind="$attrs"
    :class="[
      'bg-dark-purple-700 hover:bg-highlight-purple-500 hover:cursor-pointer text-white-purple-100 py-2 px-4 rounded-lg mx-auto sg:w-30 lg:w-40',
      $attrs.class,
    ]"
    :type="buttonType"
    @click="$emit('click', $event)"
  >
    <slot>{{ buttonText }}</slot>
  </button>
</template>

<script setup>
const props = defineProps({
  buttonText: { type: String, default: '' },
  buttonType: { type: String, default: 'button' },
})
const emit = defineEmits(['click'])
</script>
