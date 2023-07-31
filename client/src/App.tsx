import {
  BrowserRouter,
  Navigate,
  Routes,
  Route,
  Outlet,
} from "react-router-dom";
import { useSelector } from "react-redux";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Register from "./pages/admin/Register";
import Login from "./pages/Login";

const App = () => {
  const userRole: String = useSelector((state: any) => state.user.userRole);

  const AdminRoutes = () => {
    return (
      <>{userRole === "admin" ? <Outlet /> : <Navigate to="/login" />}</>
    );
  };

  const UserRoutes = () => {
    return <>{userRole === "user" ? <Outlet /> : <Navigate to="/login" />}</>;
  };

  const UnauthorizedRoutes = () => {
    return (
      <>
        {userRole === "unauthorized" ? (
          <Outlet />
        ) : (
          <Navigate to="/dashboard" />
        )}
      </>
    );
  };

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route element={<AdminRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/register" element={<Register />} />
          </Route>
          <Route element={<UserRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
          <Route element={<UnauthorizedRoutes />}>
            <Route path="/login" element={<Login />} />
          </Route>
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
