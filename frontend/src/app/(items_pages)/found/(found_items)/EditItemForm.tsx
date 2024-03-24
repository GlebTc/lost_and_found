"use client";
import { useState, useEffect } from "react";
import { useFoundItemStore } from "@/util/FoundItemStore";
import { FoundItem } from "@/types/types";

const EditItemForm = ({
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
        const response = editItem(item?.id!, formData);
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
      <h2 className="text-2xl font-bold mb-4">Edit Item - ID#</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label
            htmlFor="date_received"
            className="block text-gray-700 font-bold mb-2"
          >
            Date Received:
          </label>
          <input
            type="date"
            id="date_received"
            name="date_received"
            value={formData.date_received}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="found_location"
            className="block text-gray-700 font-bold mb-2"
          >
            Found Location:
          </label>
          <input
            type="text"
            id="found_location"
            name="found_location"
            value={formData.found_location}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="item_description"
            className="block text-gray-700 font-bold mb-2"
          >
            Item Description:
          </label>
          <textarea
            id="item_description"
            name="item_description"
            value={formData.item_description}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="received_by"
            className="block text-gray-700 font-bold mb-2"
          >
            Received By:
          </label>
          <input
            type="text"
            id="received_by"
            name="received_by"
            value={formData.received_by}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label
            htmlFor="turned_in_by"
            className="block text-gray-700 font-bold mb-2"
          >
            Turned In By:
          </label>
          <input
            type="text"
            id="turned_in_by"
            name="turned_in_by"
            value={formData.turned_in_by}
            onChange={handleChange}
            className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
          />
        </div>
        <div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring focus:border-blue-500"
          >
            Edit Item
          </button>
        </div>
      </form>
    </div>
  );
};

export default EditItemForm;
