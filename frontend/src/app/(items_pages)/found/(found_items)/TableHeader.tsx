"use client";
import { useUserStore } from "@/util/userStore";

const TableHeader = () => {

  const { user } = useUserStore();


  return (
    <thead>
      <tr className="bg-gray-200">
        <th className="border border-gray-500 px-4 py-2">Date Received</th>
        <th className="border border-gray-500 px-4 py-2">Item ID #</th>
        <th className="border border-gray-500 px-4 py-2">Found Location</th>
        <th className="border border-gray-500 px-4 py-2">Item Description</th>
        <th className="border border-gray-500 px-4 py-2">Received By</th>
        <th className="border border-gray-500 px-4 py-2">Turned In By</th>
        <th className="border border-gray-500 px-4 py-2">Edit</th>
        {user?.role === "admin" && (
          <th className="border border-gray-500 px-4 py-2">Delete</th>
        )}
        <th className="border border-gray-500 px-4 py-2">Release</th>
      </tr>
    </thead>
  );
};

export default TableHeader;
