import { reactive } from 'vue';
import axios from 'axios';
import type { User } from './types';

interface UserState {
  user: User | null;
  allUsers: User[];
  isLoading: boolean;
}

const initialState: UserState = {
  user: null,
  allUsers: [],
  isLoading: false,
};

const state = reactive<UserState>({ ...initialState });

const actions = {
  async login(email: string, password: string) {
    try {
      const response = await axios.post<User>(
        'http://127.0.0.1:8000/accounts/login/',
        { email, password }
      );
      state.user = response.data;
      return response.data;
    } catch (error) {
      console.error('Login Error:', error);
    }
  },
  async logout() {
    state.user = null;
  },
  async register(email: string, password: string) {
    try {
      const response = await axios.post<User>(
        'http://127.0.0.1:8000/accounts/register/',
        { email, password }
      );
      state.user = response.data;
    } catch (error) {
      console.error('Register Error:', error);
    }
  },
  async fetchAllUsers() {
    try {
      const response = await axios.get<User[]>(
        'http://127.0.0.1:8000/accounts/'
      );
      state.allUsers = response.data;
    } catch (error) {
      console.error('Fetch All Users Error:', error);
    }
  },
  async editUser(userId: string) {
    try {
      const response = await axios.put<User>(
        `http://127.0.0.1:8000/accounts/edit/${userId}/`
      );
      state.user = response.data;
    } catch (error) {
      console.error('Edit User Error:', error);
    }
  },
};

export default {
  state,
  ...actions,
};
