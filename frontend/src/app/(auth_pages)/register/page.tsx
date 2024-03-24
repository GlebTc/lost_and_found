"use client";
import { useState, FormEvent } from "react";
import { useUserStore } from "@/util/userStore";

const Register: React.FC = () => {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const { register } = useUserStore();

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        register(email, password);
    
        //Clear the form
        setEmail("");
        setPassword("");
      };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4">Register</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 font-bold mb-2">
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
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-green-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-green-500"
        >
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;
