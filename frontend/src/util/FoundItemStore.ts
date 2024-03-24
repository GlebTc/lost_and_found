import { create } from "zustand";
import axios from "axios";
import { FoundItem } from "@/types/types";

interface FoundItemState {
  foundItems: FoundItem[];
  isLoading: boolean;
  addItem: (item: FoundItem) => void;
  fetchAllFoundItems: () => void;
  deleteItem: (itemId: number) => void;
  editItem: (itemId: number, item: FoundItem) => void;
}

export const useFoundItemStore = create<FoundItemState>((set) => ({
  foundItems: [],
  isLoading: false,
  addItem: async (item) => {
    try {
      const response = await axios.post<FoundItem>(
        "http://127.0.0.1:8000/found-items/add/",
        item
      );
      set((state) => ({
        foundItems: [...state.foundItems, response.data],
      }));
    } catch (error) {
      console.error("Create Item Error:", error);
    }
  },
  fetchAllFoundItems: async () => {
    try {
      const response = await axios.get<FoundItem[]>(
        "http://127.0.0.1:8000/found-items/"
      );
      set({ foundItems: response.data });
    } catch (error) {
      console.error("Fetch All Items Error:", error);
    }
  },
  deleteItem: async (foundItemId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/found-items/delete/${foundItemId}/`);
      set((state) => ({
        foundItems: state.foundItems.filter((item) => item.id !== foundItemId),
      }));
    } catch (error) {
      console.error("Delete Item Error:", error);
    }
  },
    editItem: async (foundItemId, item) => {
    try {
      const response = await axios.put<FoundItem>(
        `http://127.0.0.1:8000/found-items/edit/${foundItemId}/`,
        item
        );
        set((state) => ({
            foundItems: state.foundItems.map((item) =>
                item.id === foundItemId ? response.data : item
            ),
            }));
    } catch (error) {
        console.error("Edit Item Error:", error);
        }
    }
}));
