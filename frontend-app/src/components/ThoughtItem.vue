<script setup>
import { computed } from 'vue';

// Определяем, какие props компонент ожидает получить от родителя
const props = defineProps({
  thought: {
    type: Object,
    required: true,
  },
});

// Форматируем дату для более приятного отображения
const formattedDate = computed(() => {
  return new Date(props.thought.created_at).toLocaleString();
});
</script>

<template>
  <div class="bg-white/10 p-4 my-3 rounded-lg shadow-md text-left transition hover:bg-white/20">
    <p class="text-gray-200 text-lg">{{ thought.content }}</p>
    <p class="text-xs text-gray-400 mt-2 text-right">{{ formattedDate }}</p>
  </div>
</template>

<style scoped>
/* Стили в <style scoped> применяются только к этому компоненту */
</style>