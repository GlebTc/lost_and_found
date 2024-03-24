"use client";
import { useState } from "react";
import { useUserStore } from "@/util/userStore";

const Login: React.FC = () => {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const { login } = useUserStore();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    login(email, password);

    //Clear the form
    setEmail("");
    setPassword("");
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <>
        <form onSubmit={handleSubmit}>
          <h2 className="text-2xl font-bold mb-4">Login</h2>

          <div className="mb-4">
            <label
              htmlFor="email"
              className="block text-gray-700 font-bold mb-2"
            >
              Email
            </label>
            <input
              type="text"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
              placeholder="Enter your email"
              required
            />
          </div>
          <div className="mb-6">
            <label
              htmlFor="password"
              className="block text-gray-700 font-bold mb-2"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
              placeholder="Enter your password"
              autoComplete="on"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-500"
          >
            Login
          </button>
        </form>
      </>
    </div>
  );
};

export default Login;