// https://frontendshape.com/post/react-mui-5-login-page-example

import React, { useState, ChangeEvent } from "react";
import {
  Button,
  TextField,
  FormControlLabel,
  Checkbox,
  Link,
  Grid,
  Box,
  Typography,
  Container,
} from "@mui/material";
import { userLogin } from "../api/userApis";
import  { useDispatch } from "react-redux";
import { userRoleAdmin, userRoleUser, userRoleUnauthorized } from "../redux/slices/userRoleSlice";

interface loginProps {
  user_email: string;
  user_password: string;
}

export default function Login() {
  const dispatch = useDispatch();
  const [error, setError] = useState<string>("");
  const [loginValues, setLoginValues] = useState<loginProps>({
    user_email: "",
    user_password: "",
  });

  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    setLoginValues({ ...loginValues, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const response = await userLogin(loginValues);
      console.log(response.data.userInfo.user_role);
      if (response.data.userInfo.user_role === "admin") {
        dispatch(userRoleAdmin(response.data.userInfo.user_role));
      } else if (response.data.userInfo.user_role === "user") {
        dispatch(userRoleUser(response.data.userInfo.user_role));
      } else {
        dispatch(userRoleUnauthorized(response.data.userInfo.user_role));
      }
      localStorage.setItem("userRole", JSON.stringify(response.data.userInfo.user_role))
      console.log(response.data.userInfo);
    } catch (error: any) {
      setError(error.response.data.errors[0].msg);
      setTimeout(() => {
        setError("");
      }, 1000);
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          Log in
        </Typography>
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="user_email"
            autoComplete="email"
            autoFocus
            value={loginValues.user_email}
            onChange={onChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="user_password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={loginValues.user_password}
            onChange={onChange}
          />
          {error && (
            <Box
              sx={{
                backgroundColor: "#ffe6e6", // Light red background color
                padding: "10px", // Add some padding to the box
                borderRadius: "4px", // Add rounded corners to the box
                marginTop: "10px", // Add some space between the textfield and the box
              }}
            >
              <Typography variant="body1" sx={{ color: "red" }}>
                {error}
              </Typography>
            </Box>
          )}
          <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            Log In
          </Button>
          <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2">
                Forgot password?
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}
