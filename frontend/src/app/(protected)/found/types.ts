// components/found/types.ts

export interface Item {
    id: string;
    title: string;
    description?: string | null;
    item_img_url?: string | null;
    status: 'lost' | 'found' | 'claimed';
    owner_identified: boolean;
    owner_name?: string | null;
    owner_contact?: string | null;
    date_reported_turned_in: string;
    date_claimed_returned: string;
    accepted_by: string | null;
    accepted_by_email: string;
    turned_in_by_name?: string | null;
    turned_in_by_phone?: string | null;
    claimed_by_id_verified: boolean;
    claimed_by: string;
    item_returned_by: string | null;
    item_returned_by_name?: string | null;
    site: number | null;
    building: number | null;
    level: number | null;
    department: number | null;
  }
  