"use client";
import { useState, useEffect } from "react";
import { useFoundItemStore } from "@/util/FoundItemStore";
import { FoundItem } from "@/types/types";

const ReleaseItemForm = ({
  setIsModalOpen,
  item,
}: {
  setIsModalOpen: any;
  item?: FoundItem;
}) => {
  const { fetchAllFoundItems, editItem } = useFoundItemStore();
  const [formData, setFormData] = useState<FoundItem>({});

  useEffect(() => {
    if (item) {
      setFormData(item);
    }
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const updatedFormData = { ...formData, archived: true };
      const response = editItem(item?.id!, updatedFormData);
    } catch (error) {
      console.error("Error adding item:", error);
    }

    fetchAllFoundItems(); // Fetch items when modal is closed
    setIsModalOpen(false); // Close the modal
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <button
        className="absolute top-2 right-2 bg-red-500 text-white font-bold py-2 px-4 rounded-full focus:outline-none focus:ring focus:border-blue-500"
        onClick={() => setIsModalOpen(false)}
      >
        Close
      </button>
      <h2 className="text-2xl font-bold mb-4">Release Item - ID#</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="claimed_by"
            className="block text-gray-700 font-bold mb-2"
          >
            Claimed By
          </label>
          <input
            type="text"
            id="claimed_by"
            name="claimed_by"
            value={formData.claimed_by}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="released_by"
            className="block text-gray-700 font-bold mb-2"
          >
            Released By
          </label>
          <input
            type="text"
            id="released_by"
            name="released_by"
            value={formData.released_by}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="date_released"
            className="block text-gray-700 font-bold mb-2"
          >
            Date Released
          </label>
          <input
            type="date"
            id="date_released"
            name="date_released"
            value={formData.date_released}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-500"
          >
            Release and Archive Item
          </button>
        </div>
      </form>
    </div>
  );
};

export default ReleaseItemForm;
