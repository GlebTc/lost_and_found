import { create } from "zustand";
import axios from "axios";
import { User } from "@/types/types";

interface UserState {
  user: User | null;
  allUsers: User[];
  login: (email: string, password: string) => void;
  register: (email: string, password: string) => void;
  logout: () => void;
  fetchAllUsers: () => void;
  editUser: (userId: string) => void;
  isLoading: boolean; // Type declaration for isLoading
}

export const useUserStore = create<UserState>((set) => ({
  user: null,
  isLoading: false,
  allUsers: [],

  // User Login Function in Zustand to be passed into the login component, takes an email and a password and then sets response to the user state.

  login: async (email, password) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/accounts/login/",
        { email, password }
      );
      set({ user: response.data });
    } catch (error) {
      console.error("Login Error:", error);
    }
  },
  logout: () => set({ user: null }),
  register: async (email, password) => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/accounts/register/",
        { email, password }
      );
      set({ user: response.data });
    } catch (error) {
      console.error("Register Error:", error);
    }
  },
  fetchAllUsers: async () => {
    try {
      const response = await axios.get<User[]>(
        "http://127.0.0.1:8000/accounts/"
      );
      set({ allUsers: response.data });
    } catch (error) {
      console.error("Fetch All Users Error:", error);
    }
  },
  editUser: async (userId) => {
    try {
      const response = await axios.put<User>(
        `http://127.0.0.1:8000/accounts/edit/${userId}/`
      );
      set({ user: response.data });
    } catch (error) {
      console.error("Edit User Error:", error);
    }
  },
}));
