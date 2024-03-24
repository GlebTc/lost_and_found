export interface FoundItem {
    id?: number;
    date_received?: string;
    log_item_number?: string;
    found_location?: string;
    item_description?: string;
    received_by?: string;
    turned_in_by?: string;
    claimed_by?: string;
    released_by?: string;
    date_released?: string;
    archived?: boolean;
  }
  
  export interface User {
    user?: any;
    success?: boolean;
    id?: string;
    message?: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    is_active_user?: boolean;
    role?: string;
  }
  
  
  