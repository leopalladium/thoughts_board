<template>
  <form @submit.prevent="handleSubmit" class="mb-8">
    <div class="flex flex-col gap-4">
      <textarea
          v-model="newThoughtContent"
          name="content"
          placeholder="what don't you talk about?"
          required
          class="w-full p-3 bg-gray-900 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
          rows="3"
      ></textarea>
      <button type="submit" :disabled="isLoading" class="py-2 px-4 bg-blue-600 hover:bg-blue-700 rounded-lg transition disabled:opacity-50">
        {{ isLoading ? 'posting...' : 'share' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const newThoughtContent = ref('');
const isLoading = ref(false);

// Определяем событие, которое компонент может сгенерировать
const emit = defineEmits(['thought-added']);

const handleSubmit = async () => {
  if (newThoughtContent.value.trim() === '') return;

  isLoading.value = true;
  try {
    // Вместо прямого вызова axios, мы передаем данные в родительский компонент
    emit('thought-added', { content: newThoughtContent.value });
    newThoughtContent.value = ''; // Очищаем поле после успешной отправки
  } catch (error) {
    console.error("Ошибка при отправке мысли:", error);
    // Можно добавить обработку ошибок для пользователя
  } finally {
    isLoading.value = false;
  }
};
</script>