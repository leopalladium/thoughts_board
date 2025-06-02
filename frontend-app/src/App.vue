<template>
  <main class="container mx-auto max-w-3xl">
    <header class="text-center my-12">
      <h1 class="text-5xl font-bold mb-2 font-mono">Thought Board</h1>
      <p class="text-gray-400">Простое приложение на FastAPI и Vue.js</p>
    </header>

    <thought-form @thought-added="addThought" />

    <div v-if="isLoading" class="text-center text-gray-500">Загрузка мыслей...</div>
    <div v-if="error" class="text-center text-red-500">{{ error }}</div>

    <div v-if="thoughts.length" class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
      <thought-card
          v-for="thought in thoughts"
          :key="thought.id"
          :thought="thought"
      />
    </div>
    <div v-else-if="!isLoading && !error" class="text-center text-gray-500 mt-8">
      Пока мыслей нет. Станьте первым!
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ThoughtCard from './components/ThoughtCard.vue';
import ThoughtForm from './components/ThoughtForm.vue';

const API_URL = "https://klimentsi.live/thoughts"; // URL вашего FastAPI сервера

const thoughts = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Функция для загрузки мыслей с сервера
const fetchThoughts = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get(API_URL);
    thoughts.value = response.data;
    error.value = null;
  } catch (err) {
    console.error("Ошибка при загрузке мыслей:", err);
    error.value = 'Не удалось загрузить мысли. Попробуйте обновить страницу.';
  } finally {
    isLoading.value = false;
  }
};

// Функция для добавления новой мысли
const addThought = async (thoughtData) => {
  try {
    const response = await axios.post(API_URL, thoughtData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    // Добавляем новую мысль в начало списка без перезагрузки всей страницы
    thoughts.value.unshift(response.data);
  } catch (err) {
    console.error("Ошибка при добавлении мысли:", err);
  }
};

// Загружаем мысли, когда компонент монтируется
onMounted(fetchThoughts);
</script>

<style>
/* Можно оставить общие стили, если они нужны */
body {
  background-color: #1a202c;
  color: #e2e8f0;
}
h1 {
  font-family: 'Space Mono', monospace;
}
</style>