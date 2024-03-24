"use client";
import { useState, useEffect } from "react";
import { useUserStore } from "@/util/userStore";
import { useFoundItemStore } from "@/util/FoundItemStore";
import AccessUnauthorized from "@/app/components/reusable/AccessUnauthorized";
import TableHeader from "./(found_items)/TableHeader";
import TableBody from "./(found_items)/TableBody";
import ArchivedTableBody from "./(archived_items)/ArchivedTableBody";
import ArchivedTableHeader from "./(archived_items)/ArchivedTableHeader";
import RefreshingDatabase from "@/app/components/reusable/RefreshingDatabase";
import Modal from "@/app/components/reusable/Modal";
import AddItemForm from "./(found_items)/AddItemForm";

const Found = () => {
  const { user } = useUserStore();
  const { foundItems, fetchAllFoundItems, isLoading, deleteItem } =
    useFoundItemStore();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [showArchived, setShowArchived] = useState(false);

  useEffect(() => {
    fetchAllFoundItems();
  }, []);

  const handleAddItemClick = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleDeleteItemClick = (itemId: number) => {
    deleteItem(itemId); // Call deleteItem action with itemId
  };

  const handleShowArchived = () => {
    setShowArchived(!showArchived);
  };

  if (!user || !user.role) {
    return <AccessUnauthorized />;
  }
  return (
    <div>
      <h1 className="text-3xl font-bold mb-4 text-center">Found Items</h1>
      <div className="flex justify-between mb-4">
        <button
          onClick={handleAddItemClick}
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        >
          Add Item
        </button>
        {user.role === "admin" &&
          (showArchived ? (
            <button
              onClick={handleShowArchived}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Hide Archived
            </button>
          ) : (
            <button
              onClick={handleShowArchived}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Show Archived
            </button>
          ))}
      </div>
      <div className="overflow-x-auto">
        {isLoading ? (
          <RefreshingDatabase />
        ) : (
          <table className="table-auto w-full border-collapse border border-gray-500">
            {showArchived ? <ArchivedTableHeader /> : <TableHeader />}
            {showArchived ? (
              <ArchivedTableBody
                items={foundItems}
                handleDeleteItemClick={handleDeleteItemClick}
                user={user}
              />
            ) : (
              <TableBody
                items={foundItems}
                handleDeleteItemClick={handleDeleteItemClick}
                user={user}
              />
            )}
          </table>
        )}
      </div>
      <Modal isOpen={isModalOpen} onClose={handleCloseModal}>
        <AddItemForm setIsModalOpen={setIsModalOpen} />
      </Modal>
    </div>
  );
};

export default Found;
