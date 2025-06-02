<script setup>
import { ref, onMounted } from 'vue';
import ApiService from '@/services/ApiService';
import ThoughtBubble from '@/components/ThoughtBubble.vue';

const newThoughtContent = ref('');
const thoughts = ref([]);

const fetchThoughts = async () => {
  try {
    const response = await ApiService.getThoughts();
    thoughts.value = response.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  } catch (error) {
    console.error('Ошибка при получении мыслей:', error);
  }
};

const postThought = async () => {
  if (newThoughtContent.value.trim() === '') {
    return;
  }
  try {
    const newThought = await ApiService.postThought(newThoughtContent.value);
    thoughts.value.push(newThought);
    newThoughtContent.value = '';
    setTimeout(() => {
      const chatContainer = document.querySelector('.chat-container');
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    }, 0);
  } catch (error) {
    console.error('Ошибка при отправке мысли:', error);
  }
};

onMounted(() => {
  fetchThoughts();
});
</script>

<template>
  <div class="container-fluid flex flex-col h-full p-0">
    <main class="flex-1 overflow-hidden bg-gray-100 dark:bg-gray-900">
      <div class="chat-container h-full overflow-y-auto p-4 space-y-4">
        <ThoughtBubble
            v-for="thought in thoughts"
            :key="thought.id"
            :thought="thought"
        />
      </div>
    </main>

    <footer class="p-4 bg-gray-200 dark:bg-gray-800 shadow-lg">
      <form @submit.prevent="postThought" class="flex gap-2">
        <input
            v-model="newThoughtContent"
            type="text"
            placeholder="Напишите новую мысль..."
            aria-label="New thought"
            class="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        />
        <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out">
          Отправить
        </button>
      </form>
    </footer>
  </div>
</template>

<style scoped>
.chat-container {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}
</style>