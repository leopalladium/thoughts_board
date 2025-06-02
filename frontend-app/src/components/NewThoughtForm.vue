<script setup>
import { ref } from 'vue';

const newThoughtContent = ref('');

// Определяем событие, которое компонент может отправить наверх
const emit = defineEmits(['thought-added']);

const handleSubmit = () => {
  if (newThoughtContent.value.trim() === '') return;

  // Отправляем событие с содержимым новой мысли
  emit('thought-added', newThoughtContent.value);

  // Очищаем поле ввода
  newThoughtContent.value = '';
};
</script>

<template>
  <form @submit.prevent="handleSubmit" class="mb-8 flex flex-col sm:flex-row gap-2">
    <input
        v-model="newThoughtContent"
        type="text"
        placeholder="О чем вы думаете?"
        class="flex-grow bg-gray-700 text-white placeholder-gray-400 border border-gray-600 rounded-md py-2 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
    <button
        type="submit"
        class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition"
    >
      Поделиться
    </button>
  </form>
</template>