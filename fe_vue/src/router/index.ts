import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import Home from '@/views/Home.vue';
import LostItems from '@/views/LostItems.vue';
import FoundItems from '@/views/FoundItems.vue';
import AdminPanel from '@/views/AdminPanel.vue';
import Login from '@/views/Login.vue';

const routes: RouteRecordRaw[] = [
  { path: '/', component: Home },
  { path: '/lost-items', component: LostItems },
  { path: '/found-items', component: FoundItems },
  { path: '/admin', component: AdminPanel },
  { path: '/login', component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
