<script setup>
import { ref, onMounted } from 'vue';
import api from './services/api.js'; // Наш сервис для API
import NewThoughtForm from './components/NewThoughtForm.vue';
import ThoughtList from './components/ThoughtList.vue';

// Реактивная переменная для хранения списка мыслей
const thoughts = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Функция для загрузки мыслей с сервера
const fetchThoughts = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    const response = await api.getThoughts();
    thoughts.value = response.data;
  } catch (err) {
    console.error("Ошибка при загрузке мыслей:", err);
    error.value = "Не удалось загрузить мысли. Попробуйте позже.";
  } finally {
    isLoading.value = false;
  }
};

// Функция для обработки добавления новой мысли
const handleThoughtAdded = async (content) => {
  try {
    const response = await api.createThought(content);
    // Добавляем новую мысль в начало списка без перезагрузки всей страницы
    thoughts.value.unshift(response.data);
  } catch (err) {
    console.error("Ошибка при создании мысли:", err);
    // Здесь можно показать пользователю ошибку
  }
};

// Загружаем мысли при первом рендере компонента
onMounted(() => {
  fetchThoughts();
});
</script>

<template>
  <div id="app-container" class="w-full min-h-screen bg-gray-900 text-white p-4 sm:p-8">
    <header class="text-center mb-12">
      <h1 class="text-4xl sm:text-5xl font-bold font-['Poiret_One']">Доска Мыслей</h1>
      <p class="text-gray-400">Делитесь своими идеями со всем миром</p>
    </header>

    <main class="max-w-3xl mx-auto">
      <NewThoughtForm @thought-added="handleThoughtAdded" />

      <div v-if="isLoading" class="text-center text-gray-500">Загрузка...</div>
      <div v-if="error" class="text-center text-red-500">{{ error }}</div>

      <ThoughtList v-if="!isLoading && !error" :thoughts="thoughts" />
    </main>
  </div>
</template>

<style>
/* В src/style.css теперь можно оставить только импорт Tailwind
  и самые базовые стили для body/html, если они нужны.
  Большинство стилей лучше делать с помощью утилит Tailwind прямо в шаблонах.
  @import "tailwindcss"; уже есть в вашем style.css.
  Шрифты уже подключены в index.html.
*/
</style>