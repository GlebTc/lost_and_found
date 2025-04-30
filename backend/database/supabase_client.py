# database/client.py

import os
from supabase import create_client, Client

SUPABASE_PROJECT_URL = os.getenv("SUPABASE_PROJECT_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_ANON_API_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)
supabase_admin: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_SERVICE_ROLE_KEY)