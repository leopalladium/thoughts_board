import axios from 'axios';

// Настройте базовый URL для API. VITE_API_URL нужно будет добавить
// в .env файл в папке frontend-app, например:

// Задаем постоянный адрес вашего API
const API_URL = 'https://api.klimentsi.live';

const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default {
    // Получить все "мысли"
    getThoughts() {
        return apiClient.get('/thoughts/');
    },
    // Создать новую "мысль"
    createThought(content) {
        return apiClient.post('/thoughts/', { content });
    },
};