"use client";
import { useEffect, useState } from "react";
import { useUserStore } from "@/util/userStore";
import RefreshingDatabase from "@/app/components/reusable/RefreshingDatabase";
import EditUserForm from "./EditUserForm";
import Modal from "@/app/components/reusable/Modal";
import { User } from "@/types/types";

const formatEmail = (email: string) => {
  const atIndex = email.indexOf("@");
  if (atIndex !== -1) {
    const firstLetter = email.charAt(0);
    const domain = email.substring(atIndex);
    const hiddenLength = email.substring(1, atIndex).length; // Length of characters to hide
    const asterisks = "*".repeat(hiddenLength); // Generate asterisks based on hidden length
    return `${firstLetter}${asterisks}${domain}`;
  }
  return email;
};



const Accounts: React.FC = () => {
  const { allUsers, fetchAllUsers, isLoading, user } = useUserStore();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const handleEditUserClick = (user: User) => {
    setSelectedUser(user); // Set the selected user when clicked
    setIsModalOpen(true); // Open the modal
  };

  const handleCloseModal = () => {
    setSelectedUserId(null);
    setIsModalOpen(false);
  };

  useEffect(() => {
    fetchAllUsers();
  }, []);

  if (!user || user.role !== "admin") {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex justify-center flex-col bg-red-300 text-black font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-300 w-fit mx-auto text-center">
          <p>You are not authorized to view this page</p>
          <p>Please login to continue</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center">User Accounts</h1>
      {isLoading ? (
        <RefreshingDatabase />
      ) : (
        <div>
          {allUsers.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-bold mb-4">All Users:</h2>
              <ul className="bg-gray-100 rounded-lg p-4">
                {allUsers.map((user) => (
                  <li key={user.id} className="mb-4">
                    <div className="border-b-2 pb-2 flex justify-between">
                      <div>
                        <p>
                          <strong>Unique ID:</strong> {user.id}
                        </p>
                        <p>
                          <strong>Email:</strong>
                          {user.email ? formatEmail(user.email) : ""}
                        </p>
                        <p>
                          <strong>Role:</strong> {user.role}
                        </p>
                        <p>
                          <strong>First Name:</strong> {user.first_name}
                        </p>
                        <p>
                          <strong>Last Name:</strong> {user.last_name}
                        </p>
                      </div>
                      <div className="flex justify-end mt-2 items-end">
                        <button
                          className="mr-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
                          onClick={() => handleEditUserClick(user)}
                        >
                          Edit
                        </button>

                        <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                          Delete
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
      <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
        <EditUserForm setIsModalOpen={setIsModalOpen} user={selectedUser}/>
      </Modal>
    </div>
  );
};

export default Accounts;
