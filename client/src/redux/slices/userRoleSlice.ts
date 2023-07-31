import { createSlice, Slice } from "@reduxjs/toolkit";

const userRoleFromLocalStorage = () => {
  const userRole = localStorage.getItem("userRole");

  if (userRole && JSON.parse(userRole) === "admin") {
    return "admin";
  } else if (userRole && JSON.parse(userRole) === "user") {
    return "user";
  } else {
    return "unauthorized";
  }
};

interface UserState {
  userRole: "admin" | "user" | "unauthorized";
}

const initialState: UserState = {
  userRole: userRoleFromLocalStorage(),
}

export const userRoleSlice: Slice = createSlice({
  name: "userRole",
  initialState,
  reducers: {
    userRoleAdmin: (state) => {
      state.userRole = "admin";
    },
    userRoleUser: (state) => {
      state.userRole = "user";
    },
    userRoleUnauthorized: (state) => {
      state.userRole = "unauthorized";
    },
  },
});

export const {
  userRoleAdmin,
  userRoleUser,
  userRoleUnauthorized,
} = userRoleSlice.actions;

export default userRoleSlice.reducer;
