<script setup lang="ts">
import userStore from '@/util/userStore';
import { computed } from 'vue';

const isAdmin = computed(() => userStore.state.user?.role === 'admin');
const isMember = computed(() => userStore.state.user?.role === 'member');
</script>

<template>
  <div class="NAV_MEN_DESKTOP flex space-x-4">
    <RouterLink
      to="/"
      class="text-white hover:text-gray-300"
      >Home</RouterLink
    >
    <RouterLink
      to="/lost-items"
      class="text-white hover:text-gray-300"
      >Lost Items</RouterLink
    >
    <RouterLink
      to="/found-items"
      class="text-white hover:text-gray-300"
      >Found Items</RouterLink
    >
    <template v-if="isAdmin">
      <RouterLink
        to="/admin"
        class="text-white hover:text-gray-300"
        >Admin</RouterLink
      >
    </template>
  </div>
</template>
