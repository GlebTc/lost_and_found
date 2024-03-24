"use client";
import Link from "next/link";
import NavMenuDesktop from "./NavMenuDesktop";
import { useUserStore } from "@/util/userStore";

const Navbar: React.FC = () => {
  const { user, logout } = useUserStore();
  const isAdmin = user?.role === "admin";
  const isMember = user?.role === "member";

  return (
    <nav className="bg-gray-800 p-4">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center">
          <NavMenuDesktop isAdmin={isAdmin} isMember={isMember} />
          <div className="flex space-x-4">
            {isMember || isAdmin ? (
              <button
                onClick={logout}
                className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >
                Logout
              </button>
            ) : (
              <>
                <Link href="/login">
                  <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                    Login
                  </button>
                </Link>
                <Link href="/register">
                  <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                    Register
                  </button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
