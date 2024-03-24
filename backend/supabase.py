from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)