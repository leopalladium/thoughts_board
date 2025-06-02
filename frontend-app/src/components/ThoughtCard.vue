<template>
  <article class="p-6 bg-gray-800 rounded-lg shadow-md border border-gray-700">
    <p class="text-gray-300">{{ thought.content }}</p>
    <footer class="text-right text-sm text-gray-500 mt-4">
      {{ formattedDate }}
    </footer>
  </article>
</template>

<script setup>
import { computed } from 'vue';

// Определяем props, которые компонент ожидает получить
const props = defineProps({
  thought: {
    type: Object,
    required: true
  }
});

// Форматируем дату для более приятного отображения
const formattedDate = computed(() => {
  if (!props.thought.created_at) return '';
  return new Date(props.thought.created_at).toLocaleString();
});
</script>