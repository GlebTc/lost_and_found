# database/user_service.py

from database.supabase_client import supabase, supabase_admin

def get_all_profiles():
    return supabase.table("accounts_profile").select("*").execute()

def get_profile_by_id(user_id):
    return supabase_admin.table("accounts_profile").select("*").eq("id", user_id).single().execute()

def update_profile(user_id, data):
    return supabase_admin.table("accounts_profile").update(data).eq("id", user_id).execute()

def delete_profile(user_id):
    return supabase_admin.table("accounts_profile").delete().eq("id", user_id).execute()

def create_profile(data):
    return supabase_admin.table("accounts_profile").insert(data).execute()
