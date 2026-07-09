<template>
  <div>
    <div class="flex items-center justify-between">
      <label :for="id" class="block font-heading text-3xl">
        {{ label }}
      </label>
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
        :class="[
          'block w-full bg-white-purple rounded-lg px-3 py-1.5 outline-1 -outline-offset-1 focus:outline-2',
          errorMessage
            ? 'outline-error-purple focus:outline-error-purple'
            : 'outline-dark-purple focus:outline-dark-purple',
        ]"
        @input="handleInput"
        @blur="handleBlur"
      />
      <button
        type="button"
        :aria-label="
          isVisible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'
        "
        :aria-pressed="isVisible.toString()"
        :aria-controls="id"
        class="absolute inset-y-0 right-2 flex items-center"
        @click="toggleVisibility"
      >
        <Eye v-if="!isVisible" aria-hidden="true" />
        <EyeOff v-else aria-hidden="true" />
      </button>
    </div>

    <!-- Inline error message -->
    <p v-if="errorMessage" role="alert" class="mt-1 text-sm text-error-purple">
      {{ errorMessage }}
    </p>

    <!-- Password checks -->
    <ul
      v-if="props.validate && props.showRequirements"
      class="mt-2 space-y-1 text-sm"
      role="status"
    >
      <li
        v-for="(req, index) in passwordRequirements"
        :key="index"
        class="flex items-center gap-1.5"
        :class="
          req.test
            ? 'text-highlight-purple'
            : isFilled
              ? 'text-error-purple'
              : 'text-dark-purple'
        "
      >
        <span aria-hidden="true">{{ req.test ? '✓' : '✗' }}</span>
        {{ req.message }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Eye, EyeOff } from '@lucide/vue'

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
    default: 'password',
  },
  placeholder: {
    type: String,
    default: '',
  },
  autocomplete: {
    type: String,
    default: '',
  },
  // Set to false on login
  validate: {
    type: Boolean,
    default: true,
  },
  minLength: {
    type: Number,
    default: 8,
  },
  // Set to false on confirm password field
  showRequirements: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['update:modelValue', 'valid'])

const isVisible = ref(false)
const isFilled = ref(false) // only show errors after user has interacted with the field

const passwordRequirements = computed(() => {
  const value = props.modelValue || ''
  return [
    {
      test: value.length >= props.minLength,
      message: `Minimum ${props.minLength} caractères requis.`,
    },
    {
      test: value !== value.toLowerCase(),
      message: 'Au moins une lettre majuscule requise.',
    },
    {
      test: value !== value.toUpperCase(),
      message: 'Au moins une lettre minuscule requise.',
    },
    {
      test: /\d/.test(value),
      message: 'Au moins un chiffre requis.',
    },
    {
      test: /\W/.test(value),
      message: 'Au moins un caractère spécial requis.',
    },
  ]
})

const errorMessage = computed(() => {
  if (!props.validate || !isFilled.value) return ''
  if (!props.modelValue) return 'Ce champ est requis.'
  return ''
})

const isValid = computed(
  () =>
    !props.validate ||
    (!!props.modelValue &&
      passwordRequirements.value.every((requirement) => requirement.test)),
)

const toggleVisibility = () => {
  isVisible.value = !isVisible.value
}

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
  emit('valid', isValid.value)
}

const handleBlur = () => {
  isFilled.value = true
  emit('valid', isValid.value)
}
</script>
