<script setup>
// Здесь пока ничего нет, но можно добавить контент
</script>

<template>
  <div class="p-8 text-center">
    <h1 class="text-4xl font-bold text-indigo-700 dark:text-indigo-300 mb-4">Добро пожаловать на Доску Мыслей!</h1>
    <p class="text-lg text-gray-700 dark:text-gray-300">
      Это главная страница вашего модульного сайта. Используйте навигацию, чтобы перейти к доске мыслей.
    </p>
    <router-link to="/thoughts" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out inline-block mt-6">
      Перейти к Доске Мыслей
    </router-link>
  </div>
</template>

<style scoped>
</style>