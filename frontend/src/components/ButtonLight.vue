<template>
  <button
    v-bind="$attrs"
    :class="[
      'bg-white-purple hover:cursor-pointer hover:bg-highlight-purple text-dark-purple py-2 px-4 rounded-lg mx-auto sg:w-30 lg:w-40',
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
