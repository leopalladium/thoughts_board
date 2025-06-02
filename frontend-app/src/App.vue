<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100">
    <header class="bg-indigo-700 text-white p-4 shadow-md">
      <nav class="container mx-auto flex justify-between items-center">
        <RouterLink to="/" class="text-2xl font-bold">Мой Сайт</RouterLink>
        <div class="space-x-4">
          <RouterLink to="/" class="hover:text-indigo-200 transition duration-300">Главная</RouterLink>
          <RouterLink to="/thoughts" class="hover:text-indigo-200 transition duration-300">Доска Мыслей</RouterLink>
          <RouterLink to="/about" class="hover:text-indigo-200 transition duration-300">О нас</RouterLink>
        </div>
      </nav>
    </header>

    <main class="flex-1 w-full max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <RouterView />
    </main>

    <footer class="bg-gray-800 text-white p-4 text-center shadow-inner">
      <p>&copy; 2025 Мой Модульный Сайт. Все права защищены.</p>
    </footer>
  </div>
</template>

<style scoped>
</style>