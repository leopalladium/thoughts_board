<script setup>
import { ref, reactive, onMounted } from 'vue';
import api from './services/api.js';
import NewThoughtForm from './components/NewThoughtForm.vue';
import ThoughtBoard from './components/ThoughtBoard.vue'; // Используем новый компонент

const thoughts = ref([]);
// Используем reactive для хранения позиций, т.к. это объект
const thoughtPositions = reactive({});

const isLoading = ref(true);
const error = ref(null);

// Функция для обновления позиции
const handleThoughtMoved = ({ id, left, top }) => {
  thoughtPositions[id] = { left, top };
};

// При добавлении новой мысли даем ей случайную начальную позицию
const handleThoughtAdded = async (content) => {
  try {
    const response = await api.createThought(content);
    const newThought = response.data;
    thoughts.value.unshift(newThought);
    // Задаем случайные координаты в пределах видимой части
    thoughtPositions[newThought.id] = {
      left: Math.floor(Math.random() * (window.innerWidth - 300)),
      top: Math.floor(Math.random() * (window.innerHeight - 300)),
    };
  } catch (err) {
    console.error("Ошибка при создании мысли:", err);
  }
};

const fetchThoughts = async () => {
  try {
    isLoading.value = true;
    error.value = null;
    const response = await api.getThoughts();
    thoughts.value = response.data;
    // Инициализируем позиции для загруженных мыслей
    response.data.forEach((thought, index) => {
      thoughtPositions[thought.id] = {
        left: (index * 50) % window.innerWidth,
        top: Math.floor(index / 10) * 50 + 150,
      };
    });
  } catch (err) {
    console.error("Ошибка при загрузке мыслей:", err);
    error.value = "Не удалось загрузить мысли. Попробуйте позже.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchThoughts();
});
</script>

<template>
  <div class="fixed inset-0 bg-gray-900 text-white overflow-hidden">
    <header class="absolute top-0 left-0 right-0 p-4 bg-gray-900/50 backdrop-blur-sm z-10">
      <div class="max-w-3xl mx-auto">
        <h1 class="text-3xl text-center font-['Poiret_One']">Доска Мыслей</h1>
        <NewThoughtForm @thought-added="handleThoughtAdded" />
      </div>
    </header>

    <main class="w-full h-full">
      <div v-if="isLoading" class="flex items-center justify-center h-full">Загрузка...</div>
      <div v-if="error" class="flex items-center justify-center h-full text-red-500">{{ error }}</div>

      <ThoughtBoard
          v-if="!isLoading && !error"
          :thoughts="thoughts"
          :positions="thoughtPositions"
          @thought-moved="handleThoughtMoved"
      />
    </main>
  </div>
</template>