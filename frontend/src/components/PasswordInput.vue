<template>
  <div>
    <div class="flex items-center justify-between">
      <label for="password" class="block font-heading text-3xl"
        >Mot de passe</label
      >
      <div class="text-sm"></div>
    </div>
    <div class="mt-2 relative">
      <input
        :id="id"
        :type="isVisible ? 'text' : 'password'"
        :value="modelValue"
        :name="name"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        required
        class="block w-full bg-white-purple-100 rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 outline-dark-purple-700 focus:outline-2"
        @input="updateValue"
      />
      <button
        type="button"
        :aria-label="
          isVisible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'
        "
        :aria-pressed="isVisible.toString()"
        aria-controls="password"
        class="absolute inset-y-0 right-2 flex items-center"
        @click="toggleVisibility"
      >
        <svg
          v-if="!isVisible"
          class="h-5 w-5 text-dark-purple-700 cursor-pointer"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M2.458 12C3.732 7.943 7.523 5 12 5
                        c4.477 0 8.268 2.943 9.542 7
                        -1.274 4.057-5.065 7-9.542 7
                        -4.477 0-8.268-2.943-9.542-7z"
          />
        </svg>

        <svg
          v-else
          class="h-5 w-5 text-dark-purple-700 cursor-pointer"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          aria-hidden="true"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 3l18 18M9.88 9.88
                        a3 3 0 104.24 4.24M6.18 6.18
                        A9.956 9.956 0 0112 5
                        c4.477 0 8.268 2.943
                        9.542 7a9.97 9.97 0 01-4.043 5.132"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: 'Mot de passe',
  },
  name: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  autocomplete: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue'])

const isVisible = ref(false)

const toggleVisibility = () => {
  isVisible.value = !isVisible.value
}

const updateValue = (event) => {
  emit('update:modelValue', event.target.value)
}
</script>
