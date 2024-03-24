<script setup lang="ts">
import { ref } from 'vue';
import userStore from '@/util/userStore';
import router from '@/router';

const email = ref('');
const password = ref('');

const onSubmit = async () => {
  try {
    await userStore.login(email.value, password.value);
    router.push('/');
  } catch (error) {
    console.error(error);
  }

  email.value = '';
  password.value = '';
};
</script>

<template>
  <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
    <form
      id="form"
      @submit.prevent="onSubmit"
    >
      <div class="EMAIL_LABEL_AND_INPUT mb-4">
        <label
          for="email"
          class="block text-gray-700 font-bold mb-2"
          block
          text-gray-700
          font-bold
          mb-2
          >Email</label
        >
        <input
          v-model="email"
          type="email"
          id="email"
          name="email"
          class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
        />
      </div>
      <div class="PASSWORD_LABEL_AND_INPUT mb-4">
        <label
          for="password"
          class="block text-gray-700 font-bold mb-2"
          block
          text-gray-700
          font-bold
          mb-2
          >Password</label
        >
        <input
          v-model="password"
          type="password"
          id="password"
          name="password"
          class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
        />
      </div>
      <div class="LOGIN_BUTTON">
        <button
          type="submit"
          class="w-full bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Login
        </button>
      </div>
    </form>
  </div>
</template>
