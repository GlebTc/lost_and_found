"use client";
import { useState, useEffect } from "react";
import { User } from "@/types/types";
import { useUserStore } from "@/util/userStore";

const EditUserForm = ({
  setIsModalOpen,
  user,
}: {
  setIsModalOpen: any;
  user?: any;
}) => {
  const [formData, setFormData] = useState<User>({});
  const { editUser, fetchAllUsers } = useUserStore();

  useEffect(() => {
    if (user) {
      setFormData(user);
    }
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    try {
        const response = editUser(user?.id!);
    } catch (error) {
      console.error("Error adding item:", error);
    }

    fetchAllUsers(); // Fetch items when modal is closed
    setIsModalOpen(false); // Close the modal
  };
  
  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <button
        className="absolute top-2 right-2 bg-red-500 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:ring focus:border-blue-500"
        onClick={() => setIsModalOpen(false)}
      >
        Close
      </button>
      {user ? (
        <h2 className="text-2xl font-bold mb-4">Edit User - {user.first_name} {user.last_name}</h2>
      ) : (
        <h2 className="text-2xl font-bold mb-4">Add New User</h2>
      )}
      <form>
        <div className="mb-4">
          <label
            htmlFor="email"
            className="block text-gray-700 font-bold mb-2"
          >
            Email:
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="role"
            className="block text-gray-700 font-bold mb-2"
          >
            Role:
          </label>
          <select
            id="role"
            name="role"
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          >
            <option value="member">Member</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div className="mb-4">
          <label
            htmlFor="first_name"
            className="block text-gray-700 font-bold mb-2"
          >
            First Name:
          </label>
          <input
            type="text"
            id="first_name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="last_name"
            className="block text-gray-700 font-bold mb-2"
          >
            Last Name:
          </label>
          <input
            type="text"
            id="last_name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          >
            Save
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditUserForm;
