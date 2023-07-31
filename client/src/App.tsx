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
  const userStatus: String = useSelector((state: any) => state.user.userStatus);

  const AuthorizedRoutes = () => {
    return <>{userStatus === "user" ? <Outlet /> : <Navigate to="/login" />}</>;
  };

  const UnauthorizedRoutes = () => {
    return <>{userStatus === "unauthorized" ? <Outlet /> : <Navigate to="/dashboard" />}</>;
  };

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route element={<AuthorizedRoutes />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>
          <Route element={<UnauthorizedRoutes />}>
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
          </Route>
        </Routes>
      </Layout>
    </BrowserRouter>
  );
};

export default App;
