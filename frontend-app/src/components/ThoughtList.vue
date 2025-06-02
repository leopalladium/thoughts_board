<script setup>
import ThoughtItem from './ThoughtItem.vue';

// Получаем массив "мыслей" от родительского компонента
defineProps({
  thoughts: {
    type: Array,
    required: true,
  },
});
</script>

<template>
  <div class="w-full max-w-2xl mx-auto">
    <div v-if="thoughts.length > 0">
      <ThoughtItem
          v-for="thought in thoughts"
          :key="thought.id"
          :thought="thought"
      />
    </div>
    <div v-else class="text-gray-500 mt-10">
      <p>Пока нет ни одной мысли... Будьте первым!</p>
    </div>
  </div>
</template>