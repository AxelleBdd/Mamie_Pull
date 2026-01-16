<template>
  <div
    class="flex h-full flex-col overflow-hidden rounded-xl bg-white
           shadow-sm transition border-dark-purple-700 border-1
           hover:-translate-y-1 hover:shadow-lg"
  >
    <!-- Image -->
    <div class="relative h-48 w-full bg-grey-purple-400 flex items-center justify-center overflow-hidden">
      <img
        v-if="product.image"
        :src="product.image"
        :alt="product.title"
        class="h-full w-full object-cover"
      />
      <span
        v-else
        class="text-6xl text-grey-purple-400"
      >
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
        class="mb-3 text-xl font-semibold leading-tight text-dark-purple-700 font-heading"
      >
        {{ product.title }}
      </h3>

      <p
        class="mb-5 flex-1 text-sm leading-relaxed text-dark-purple-700 font-body"
      >
        {{ truncatedDescription }}
      </p>

      <button
        @click="$emit('view-details', product.id)"
        class="mt-auto w-full rounded-lg bg-dark-purple-700 px-6 py-3
               text-sm font-medium text-white-purple-100 transition
               hover:bg-highlight-purple-500 active:scale-95"
      >
        Voir les détails
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  product: {
    type: Object,
    required: true
  },
  maxDescriptionLength: {
    type: Number,
    default: 100
  }
});

defineEmits(['view-details']);

const truncatedDescription = computed(() => {
  if (props.product.description.length <= props.maxDescriptionLength) {
    return props.product.description;
  }
  return props.product.description.substring(0, props.maxDescriptionLength) + '...';
});
</script>