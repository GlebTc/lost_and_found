import { useSelector } from "react-redux";
import { NavLink } from "react-router-dom";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";

const Navbar = () => {
  const userRole: String = useSelector((state: any) => state.user.userRole);


  // Common sx styles for NavLink
  const navLinkStyles = {
    "& a": {
      color: "inherit",
      textDecoration: "none", 
      "&:visited": {
        color: "inherit",
      },
    },
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Lost and Found
          </Typography>
          {userRole === "admin" ? (
            <>
              <Button color="inherit" sx={navLinkStyles}>
                <NavLink to="/register">Register New user</NavLink>
              </Button>
              <Button color="inherit" sx={navLinkStyles}>
                Logout
              </Button>
            </>
          ) : userRole === "user" ? (
            <>
              <Button color="inherit">Logout</Button>
            </>
          ) : (
            <Button color="inherit" sx={navLinkStyles}>
              <NavLink to="/login">Login</NavLink>
            </Button>
          )}
        </Toolbar>
      </AppBar>
    </Box>
  );
};

export default Navbar;
