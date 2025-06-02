<template>
  <main class="container mx-auto max-w-6xl">
    <header class="text-center my-12">
      <h1 class="text-5xl font-bold mb-2 font-mono">Thought Board</h1>
      <p class="text-gray-400">Поделитесь своей мыслью со вселенной</p>
    </header>

    <thought-form @thought-added="addThought" />

    <div v-if="isLoading" class="text-center text-gray-500">Загрузка мыслей...</div>
    <div v-if="error" class="text-center text-red-500">{{ error }}</div>

    <div class="relative w-full h-[600px] bg-gray-900/50 rounded-lg border border-gray-700 mt-8">
      <thought-card
          v-for="thought in thoughts"
          :key="thought.id"
          :thought="thought"
          class="absolute transition-all duration-300 ease-in-out"
          :style="getThoughtStyle(thought.id)"
      />
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue';
import axios from 'axios';
import ThoughtCard from './components/ThoughtCard.vue';
import ThoughtForm from './components/ThoughtForm.vue';

const API_URL = import.meta.env.VITE_API_URL;

const thoughts = ref([]);
const isLoading = ref(true);
const error = ref(null);
// 3. Объект для хранения случайных позиций
const thoughtPositions = reactive(new Map());

// 4. Функция для генерации и получения стилей
const getThoughtStyle = (id) => {
  if (!thoughtPositions.has(id)) {
    // Генерируем случайные top и left в процентах, чтобы карточки не вылезали за пределы
    const top = Math.floor(Math.random() * 80); // 0% to 80% to avoid overflow
    const left = Math.floor(Math.random() * 80); // 0% to 80%
    thoughtPositions.set(id, { top: `${top}%`, left: `${left}%` });
  }
  return thoughtPositions.get(id);
};


const fetchThoughts = async () => {
  try {
    isLoading.value = true;
    const response = await axios.get(API_URL);
    thoughts.value = response.data;
    error.value = null;
  } catch (err) {
    console.error("Ошибка при загрузке мыслей:", err);
    error.value = 'Не удалось загрузить мысли.';
  } finally {
    isLoading.value = false;
  }
};

const addThought = async (thoughtData) => {
  try {
    const response = await axios.post(API_URL, thoughtData);
    thoughts.value.unshift(response.data);
  } catch (err) {
    console.error("Ошибка при добавлении мысли:", err);
  }
};

onMounted(fetchThoughts);
</script>

<style>
/* Дополнительные стили, чтобы карточки не перекрывали форму */
#app {
  padding-bottom: 5rem;
}
</style>