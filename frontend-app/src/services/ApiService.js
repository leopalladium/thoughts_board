import axios from 'axios';

const API_BASE_URL = "https://api.klimentsi.live" || 'http://localhost:8000';

const ApiService = {
async getThoughts() {
try {
const response = await axios.get(`${API_BASE_URL}/thoughts/`);
return response.data;
} catch (error) {
console.error('Ошибка в ApiService при получении мыслей:', error);
throw error;
}
},

async postThought(content) {
try {
const response = await axios.post(`${API_BASE_URL}/thoughts/`, { content });
return response.data;
} catch (error) {
console.error('Ошибка в ApiService при отправке мысли:', error);
throw error;
}
},
};

export default ApiService;