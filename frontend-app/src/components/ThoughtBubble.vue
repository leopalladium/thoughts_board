<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  thought: {
    type: Object,
    required: true
  }
});

const formattedTime = computed(() => {
  const date = new Date(props.thought.created_at);
  return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
});

const formattedDate = computed(() => {
  const date = new Date(props.thought.created_at);
  return date.toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit', year: 'numeric' });
});
</script>

<template>
  <div class="flex justify-end mb-2">
    <div class="bg-indigo-500 text-white rounded-lg p-3 max-w-lg shadow-md break-words">
      <p class="text-sm">{{ thought.content }}</p>
      <div class="text-right text-xs opacity-80 mt-1">
        <span class="font-mono">{{ formattedTime }}</span>
        <span class="ml-2">{{ formattedDate }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>