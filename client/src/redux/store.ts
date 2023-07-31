import { configureStore } from "@reduxjs/toolkit";
import { userRoleSlice } from "./slices/userRoleSlice";

interface RootState {
    user: ReturnType<typeof userRoleSlice.reducer>;
  }

  export const store = configureStore({
    reducer: {
      user: userRoleSlice.reducer,
    },
  });
