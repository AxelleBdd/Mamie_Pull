<template>
  <div
    :class="['flex h-full flex-col overflow-hidden rounded-xl shadow-sm border-dark-purple-700 border-1 transition hover:-translate-y-1 hover:shadow-lg', isCardClickable ? 'cursor-pointer' : '']"
    @click="handleCardClick"
  >
    <!-- Image -->
    <div class="relative h-48 w-full bg-grey-purple-400 flex items-center justify-center overflow-hidden">
      <img
        v-if="product.image"
        :src="product.image"
        :alt="product.title"
        class="h-full w-full object-cover"
      />
      <span v-else class="text-6xl text-grey-purple-400">
        📦
      </span>
    </div>

    <!-- Content -->
    <div class="flex flex-1 flex-col bg-white-purple-100 p-5">
      <span
        class="mb-2 text-xs font-semibold uppercase tracking-wider text-dark-purple-700"
      >
        {{ product.category_name }}
      </span>

      <h3
        class="mb-2 text-2xl font-medium leading-tight text-dark-purple-700 font-heading"
      >
        {{ product.title }}
      </h3>

      <!-- Button visible only on desktop -->
      <button
        v-if="!isCardClickable"
        @click.stop="$emit('view-details', product.id)"
        class="mt-auto w-full rounded-lg bg-dark-purple-700 px-6 py-3
               text-sm font-medium font-body text-white-purple-100 transition
               lg:inline-block hover:bg-highlight-purple-500 active:scale-95"
      >
        Voir les détails
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  product: Object
});
const emit = defineEmits(['view-details']);

// Detect window size
const isCardClickable = ref(false);

const updateClickable = () => {
  // If screen width is less than 1024px (lg breakpoint), make card clickable
  isCardClickable.value = window.innerWidth < 1024;
};

const handleCardClick = () => {
  if (isCardClickable.value) {
    emit('view-details', props.product.id);
  }
};

// Window resize listener
onMounted(() => {
  updateClickable();
  window.addEventListener('resize', updateClickable);
});
onUnmounted(() => {
  window.removeEventListener('resize', updateClickable);
});
</script>
