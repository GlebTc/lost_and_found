import { createSlice, Slice } from "@reduxjs/toolkit";

const userStatusFromLocalStorage = () => {
  const userStatus = localStorage.getItem("userStatus");

  if (userStatus && JSON.parse(userStatus) === "admin") {
    return "admin";
  } else if (userStatus && JSON.parse(userStatus) === "user") {
    return "user";
  } else {
    return "unauthorized";
  }
};

interface UserState {
  userStatus: "admin" | "user" | "unauthorized";
}

const initialState: UserState = {
  userStatus: userStatusFromLocalStorage(),
}

export const userSlice: Slice = createSlice({
  name: "userStatus",
  initialState,
  reducers: {
    usetStatusAdmin: (state) => {
      state.userStatus = "admin";
    },
    userStatusUser: (state) => {
      state.userStatus = "user";
    },
    userStatusUnauthorized: (state) => {
      state.userStatus = "unauthorized";
    },
  },
});

export const {
  usetStatusAdmin,
  userStatusUser,
  userStatusUnauthorized,
} = userSlice.actions;

export default userSlice.reducer;
