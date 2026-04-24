<template>
  <button
    v-bind="$attrs"
    :class="[
      'bg-dark-purple hover:bg-highlight-purple hover:cursor-pointer text-white-purple py-2 px-4 rounded-lg mx-auto sg:w-30 lg:w-40',
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
