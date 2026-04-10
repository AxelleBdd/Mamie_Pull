<template>
  <div
    :class="[
      'flex h-full flex-col rounded-xl shadow-sm border-dark-purple-700 border overflow-hidden transition hover:-translate-y-1 hover:shadow-lg',
      isCardClickable ? 'cursor-pointer' : '',
    ]"
    @click="handleCardClick"
  >
    <!-- Image -->
    <div
      class="relative h-48 w-full bg-grey-purple-400 flex items-center justify-center overflow-hidden"
    >
      <img
        v-if="product.image"
        :src="product.image"
        :alt="product.title"
        class="h-full w-full object-cover"
      />
      <span v-else aria-hidden="true" class="text-6xl text-grey-purple-400">
        📦
      </span>
    </div>

    <!-- Content -->
    <div class="flex flex-1 flex-col bg-white-purple-100 p-5">
      <span
        class="mb-2 text-base font-semibold uppercase tracking-wider text-dark-purple-700"
      >
        {{ product.category_name }}
      </span>

      <h3
        class="mb-2 text-2xl font-medium leading-tight text-dark-purple-700 font-heading"
      >
        {{ product.title }}
      </h3>

      <!-- Button visible only on desktop -->
      <ButtonDark
        v-if="!isCardClickable"
        class="mt-auto w-full rounded-lg px-6 py-3 sm:text-lg cursor-pointer"
        :aria-label="`Voir les détails du produit ${product.title}`"
        button-type="button"
        @click="() => $emit('view-details', product.id)"
      >
        Voir les détails
      </ButtonDark>
    </div>
  </div>
</template>

<script setup>
import ButtonDark from './ButtonDark.vue'
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
})
const emit = defineEmits(['view-details'])

// Detect window size
const isCardClickable = ref(false)

const updateClickable = () => {
  // If screen width is less than 1024px (lg breakpoint), make card clickable
  isCardClickable.value = window.innerWidth < 1024
}

const handleCardClick = () => {
  if (isCardClickable.value) {
    emit('view-details', props.product.id)
  }
}

// Window resize listener
onMounted(() => {
  updateClickable()
  window.addEventListener('resize', updateClickable)
})
onUnmounted(() => {
  window.removeEventListener('resize', updateClickable)
})
</script>
