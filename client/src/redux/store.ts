import { configureStore } from "@reduxjs/toolkit";
import { userSlice } from "./slices/userSlice";

interface RootState {
    user: ReturnType<typeof userSlice.reducer>;
  }

  export const store = configureStore({
    reducer: {
      user: userSlice.reducer,
    },
  });
