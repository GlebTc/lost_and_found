import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

interface Item {
  id: string; // UUID from Django
  title: string;
  description?: string | null;
  item_img_url?: string | null;
  status: 'lost' | 'found' | 'claimed';
  owner_identified: boolean;
  owner_name?: string | null;
  owner_contact?: string | null;
  date_reported_turned_in: string; // or Date, depending on how you parse it
  date_claimed_returned: string; // or Date
  accepted_by: string | null; // foreign key to Profile (UUID)
  accepted_by_email: string;
  turned_in_by_name?: string | null;
  turned_in_by_phone?: string | null;
  claimed_by_id_verified: boolean;
  claimed_by: string;
  item_returned_by: string | null; // UUID of Profile
  item_returned_by_name?: string | null;

  site: number | null;
  building: number | null;
  level: number | null;
  department: number | null;
}

interface PaginatedResponse {
    results: Item[];
    count: number;
    next: string | null;
    previous: string | null;
  }
  
  const fetchFoundItems = async (page = 1, searchTerm = ''): Promise<PaginatedResponse> => {
    const response = await axios.get(
      `http://localhost:8000/api/v1/items/?page=${page}&q=${encodeURIComponent(searchTerm)}`,
      { withCredentials: true }
    );
    return response.data;
  };
  
  export const useFoundItems = (page: number, searchTerm: string) => {
    return useQuery<PaginatedResponse, Error>({
      queryKey: ['found-items', page, searchTerm],
      queryFn: () => fetchFoundItems(page, searchTerm),
      placeholderData: (prevData) => prevData,
      staleTime: 300000, // 5 minutes
    });
  };