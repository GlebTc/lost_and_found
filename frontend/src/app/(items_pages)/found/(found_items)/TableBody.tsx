"use client";
import { useState } from "react";
import { FoundItem } from "@/types/types";
import EditItemForm from "./EditItemForm";
import Modal from "@/app/components/reusable/Modal";
import ReleaseItemForm from "./ReleaseItemForm";
import { User } from "@/types/types";

interface Props {
  items: FoundItem[];
  handleDeleteItemClick: (itemId: number) => void;
  user: User | null;
}

const TableBody: React.FC<Props> = ({ items, handleDeleteItemClick, user }) => {
  const [isReleaseModalOpen, setIsReleaseModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedItemId, setSelectedItemId] = useState<number | null>(null);

  const handleEditItemClick = (itemId: number) => {
    setSelectedItemId(itemId);
    setIsEditModalOpen(true);
  };

  const handleReleaseItemClick = (itemId: number) => {
    setSelectedItemId(itemId);
    setIsReleaseModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedItemId(null);
    setIsReleaseModalOpen(false);
    setIsEditModalOpen(false);
  };

  // Filter items where archived is false
  const filteredItems = items.filter((item) => !item.archived);

  return (
    <tbody>
      {filteredItems.map((item) => (
        <tr key={item.id}>
          <td className="border border-gray-500 px-4 py-2">
            {item.date_received}
          </td>
          <td className="border border-gray-500 px-4 py-2 text-center">
            {item.id}
          </td>
          <td className="border border-gray-500 px-4 py-2 text-center">
            {item.found_location}
          </td>
          <td className="border border-gray-500 px-4 py-2 max-w-[35vw] break-words text-center">
            {item.item_description}
          </td>
          <td className="border border-gray-500 px-4 py-2 text-center">
            {item.received_by}
          </td>
          <td className="border border-gray-500 px-4 py-2 text-center">
            {item.turned_in_by}
          </td>

          <td className="border border-gray-500 px-4 py-2">
            <div className="flex justify-center">
              <button
                className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded"
                onClick={() => handleEditItemClick(item.id || 0)}
              >
                Edit
              </button>
            </div>
          </td>
          {user?.role === "admin" && (
            <td className="border border-gray-500 px-4 py-2">
              <div className="flex justify-center">
                <button
                  className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
                  onClick={() => handleDeleteItemClick(item.id || 0)}
                >
                  Delete
                </button>
              </div>
            </td>
          )}
          <td className="border border-gray-500 px-4 py-2">
            <div className="flex justify-center">
              <button
                className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                onClick={() => handleReleaseItemClick(item.id || 0)}
              >
                Release
              </button>
            </div>
          </td>
        </tr>
      ))}
      <Modal isOpen={isEditModalOpen} onClose={handleCloseModal}>
        {selectedItemId !== null && (
          <EditItemForm
            setIsModalOpen={setIsEditModalOpen}
            item={items.find((item) => item.id === selectedItemId)}
          />
        )}
      </Modal>
      <Modal isOpen={isReleaseModalOpen} onClose={handleCloseModal}>
        {selectedItemId !== null && (
          <ReleaseItemForm
            setIsModalOpen={setIsReleaseModalOpen}
            item={items.find((item) => item.id === selectedItemId)}
          />
        )}
      </Modal>
    </tbody>
  );
};

export default TableBody;
