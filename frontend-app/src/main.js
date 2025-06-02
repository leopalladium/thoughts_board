import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { DndProvider } from 'vue3-dnd' // --- 1. Импортируем провайдер
import { HTML5Backend } from 'react-dnd-html5-backend' // --- 2. Импортируем бэкенд

createApp(App)
    .provide(DndProvider, { backend: HTML5Backend })
    .mount('#app')