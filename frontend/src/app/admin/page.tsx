"use client";
import Link from "next/link";
import { useUserStore } from "@/util/userStore";

const Admin: React.FC = () => {
  const { user } = useUserStore();
  
  if (!user || user.role !== "admin") {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8 text-center">Admin Page</h1>
        <div className="flex justify-center">
          <p className="bg-red-300 text-black font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-300">
            You are not authorized to view this page
          </p>
        </div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">Admin Page</h1>
      <div className="flex justify-center">
        <Link href="/admin/accounts">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-300">
            Get All Users
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Admin;