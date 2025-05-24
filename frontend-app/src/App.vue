<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// URL нашего FastAPI бэкенда
// Убедитесь, что ваш FastAPI сервер запущен (обычно на http://127.0.0.1:8000)
const backendUrl = 'http://127.0.0.1:8000';

// Реактивные переменные
const thoughts = ref([]); // Список мыслей
const newThoughtContent = ref(''); // Содержимое новой мысли из поля ввода
const isLoading = ref(false);
const error = ref(null);

// Функция для загрузки мыслей с бэкенда
async function fetchThoughts() {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`${backendUrl}/thoughts/`);
    thoughts.value = response.data;
  } catch (err) {
    console.error('Ошибка при загрузке мыслей:', err);
    error.value = 'Не удалось загрузить мысли. Убедитесь, что бэкенд сервер запущен и доступен. ' + (err.message || '');
    if (err.response) {
      // Ошибка от сервера (например, 404, 500)
      error.value += ` Статус: ${err.response.status}`;
    } else if (err.request) {
      // Запрос был сделан, но ответ не получен (например, бэкенд не доступен)
      error.value += ' Бэкенд не отвечает.';
    }
  } finally {
    isLoading.value = false;
  }
}

// Функция для добавления новой мысли
async function addThought() {
  if (!newThoughtContent.value.trim()) {
    alert('Мысль не может быть пустой!');
    return;
  }
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.post(`${backendUrl}/thoughts/`, {
      content: newThoughtContent.value
    });
    thoughts.value.unshift(response.data); // Добавляем новую мысль в начало списка (оптимистичное обновление)
    newThoughtContent.value = ''; // Очищаем поле ввода
    await fetchThoughts(); // Перезагружаем список мыслей, чтобы увидеть все, включая новую
  } catch (err) {
    console.error('Ошибка при добавлении мысли:', err);
    error.value = 'Не удалось добавить мысль. ' + (err.message || '');
    if (err.response) {
      error.value += ` Статус: ${err.response.status}`;
      error.value += ` Статус: ${err.response.status}`;
    } else if (err.request) {
      error.value += ' Бэкенд не отвечает.';
    }
  } finally {
    isLoading.value = false;
  }
}

// Загружаем мысли при монтировании компонента
onMounted(() => {
  fetchThoughts();
});
</script>

<template>
  <div class="app-layout">

    <header class="app-header">
      <h1>Белый Холст Мыслей</h1>
    </header>

    <main class="thoughts-canvas"> {/* Наш "холст" */}
      <transition-group name="thought-card-animation" tag="div" class="thoughts-grid">

        <article v-for="thought in thoughts" :key="thought.id" class="thought-card">
          <p>{{ thought.content }}</p>
          <footer>
            <small>{{ new Date(thought.created_at).toLocaleString() }}</small>
          </footer>
        </article>
      </transition-group>
      <p v-if="thoughts.length === 0 && !isLoading && !error" class="no-thoughts">
        Пока мыслей нет. Напишите первую!
      </p>
      <p v-if="isLoading && thoughts.length === 0" class="loading-thoughts">Загрузка...</p>
    </main>

    <footer class="input-area">
      <form @submit.prevent="addThought" class="thought-form">
        <textarea
            v-model="newThoughtContent"
            placeholder="Ваша мысль..."
            rows="2"
            required
        ></textarea>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? '...' : 'Отправить' }}
        </button>
      </form>
      <div v-if="error" class="error-message">
        <small>{{ error }}</small>
      </div>
    </footer>

  </div>
</template>

<style scoped>
/* Общий макет приложения */
.app-layout {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Занимает всю высоту экрана */
  background-color: #ffffff; /* Белый фон для всего "холста" */
  overflow: hidden; /* Предотвращаем двойные скроллбары */
}

.app-header {
  padding: 0.75rem 1rem; /* Немного уменьшим отступы, если используем Pico по умолчанию */
  text-align: center;
  border-bottom: 1px solid var(--pico-muted-border-color, #e1e1e1); /* Линия из Pico */
  flex-shrink: 0; /* Заголовок не должен сжиматься */
}

.app-header h1 {
  margin: 0;
  font-size: 1.25rem; /* Немного меньше для компактности */
  color: var(--pico-h1-color, #1d2d35); /* Цвет из Pico */
}

/* Холст для мыслей */
.thoughts-canvas {
  flex-grow: 1; /* Занимает все доступное пространство */
  overflow-y: auto; /* Позволяет прокручивать мысли, если их много */
  padding: 1rem; /* Отступы внутри холста */
  background-color: #ffffff; /* Явно белый фон холста */
}

.thoughts-grid {
  display: flex;
  flex-wrap: wrap; /* Карточки будут переноситься на новую строку */
  gap: 1rem; /* Пространство между карточками */
  align-content: flex-start; /* Карточки начинаются сверху */
}

/* Стилизация карточки мысли */
.thought-card {
  /* Pico <article> уже дает базовые стили, мы их дополняем */
  background-color: var(--pico-card-background-color, #f8f9fa); /* Цвет фона карточки из Pico или свой */
  border: 1px solid var(--pico-card-border-color, #e9ecef); /* Граница из Pico */
  border-radius: 12px; /* Скругленные углы! */
  padding: 1rem 1.25rem; /* Внутренние отступы */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* Мягкая тень */
  width: calc(33.333% - 1rem); /* Примерно 3 карточки в ряд, можно менять */
  /* Можно добавить min-width/max-width для адаптивности */
  min-width: 280px; /* Минимальная ширина карточки */
  box-sizing: border-box; /* Чтобы padding и border не влияли на общую ширину */
}

.thought-card p {
  margin-bottom: 0.5rem;
  color: var(--pico-color, inherit);
}

.thought-card footer small {
  color: var(--pico-secondary, #73828c); /* Цвет из Pico */
}

.no-thoughts, .loading-thoughts {
  text-align: center;
  width: 100%;
  padding: 2rem;
  color: var(--pico-secondary, #73828c);
}

/* Область ввода снизу */
.input-area {
  padding: 1rem;
  background-color: var(--pico-form-element-background-color, #f1f3f5); /* Фон из Pico для форм */
  border-top: 1px solid var(--pico-muted-border-color, #e1e1e1);
  flex-shrink: 0; /* Область ввода не должна сжиматься */
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05); /* Небольшая тень сверху */
}

.thought-form {
  display: flex;
  gap: 0.75rem; /* Пространство между textarea и кнопкой */
  align-items: flex-start; /* Выравнивание по верху */
}

.thought-form textarea {
  flex-grow: 1;
  /* Pico уже стилизует textarea, можно добавить min-height если нужно */
  min-height: 40px; /* Чтобы не была слишком низкой */
  resize: none; /* Отключаем изменение размера пользователем, если нужно */
}

.thought-form button {
  /* Pico стилизует кнопку, здесь можно только специфичные调整 */
  white-space: nowrap; /* Чтобы текст кнопки не переносился */
}

.error-message {
  margin-top: 0.5rem;
  color: var(--pico-invalid-color, #d83636); /* Цвет ошибки из Pico */
  text-align: center;
}

/* Анимация для "хуяряться" */
.thought-card-animation-enter-active,
.thought-card-animation-leave-active {
  transition: all 0.5s ease;
}
.thought-card-animation-enter-from,
.thought-card-animation-leave-to {
  opacity: 0;
  transform: translateY(30px) scale(0.95); /* Вылетает снизу и немного увеличивается */
}
/* Для анимации перемещения, если порядок меняется */
.thought-card-animation-move {
  transition: transform 0.5s ease;
}
</style>