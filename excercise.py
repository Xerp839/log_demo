import time

# --- DUMMY HELPER ---
def get_user_profile(user_id):
    # Simulating a database fetch
    time.sleep(0.2)
    if user_id == "ID_05":
        return None # Simulated failure
    return {"id": user_id, "role": "admin", "email": f"{user_id}@company.com"}

# --- MAIN LOGIC ---
def sync_user_permissions():
    users = ["ID_01", "ID_02", "ID_03", "ID_04", "ID_05"]
    
    for user_id in users:
        profile = get_user_profile(user_id)
        
        #  CRASH POINT: If profile is None (ID_05), the next line crashes the app
        if profile['role'] == "admin":
            print(f"Syncing permissions for {user_id}")
            time.sleep(0.1)
    
    print("Process finished!")

if __name__ == "__main__":
    sync_user_permissions()