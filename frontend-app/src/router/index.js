import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import ThoughtBoardView from '@/views/ThoughtBoardView.vue';

const routes = [
    {
        path: '/',
        name: 'Home',
        component: HomeView,
    },
    {
        path: '/thoughts',
        name: 'ThoughtBoard',
        component: ThoughtBoardView,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;