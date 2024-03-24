<script setup lang="ts">
import NavMenuDesktop from './NavMenuDesktop.vue';
import userStore from '@/util/userStore';
import { computed } from 'vue';

const isAdmin = computed(() => userStore.state.user?.role === 'admin');
const isMember = computed(() => userStore.state.user?.role === 'member');

const handleLogout = async () => {
  try {
    await userStore.logout();
  } catch (error) {
    console.error(error);
  }
};
</script>

<template>
  <nav class="bg-gray-600 p-4">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between items-center">
        <NavMenuDesktop />
        <div className="flex space-x-4">
          <template v-if="isMember || isAdmin">
            <button
              @click="handleLogout"
              className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <RouterLink to="/login">
              <button
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                Login
              </button>
            </RouterLink>
            <button
              className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            >
              Register
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<style></style>
