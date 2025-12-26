import uuid
import time
from logger_config import setup_logger # Import the setup function, not just 'log'

# Setup a dedicated logger for the exercise in 'exc_log' folder
log = setup_logger("ExerciseLogger", "exc_log")

# --- DUMMY HELPER ---
def get_user_profile(user_id, t_id):
    log.debug(f"Fetching profile from DB for {user_id}", extra={"trace_id": t_id})
    time.sleep(0.2)
    
    if user_id == "ID_05":
        return None 
    return {"id": user_id, "role": "admin", "email": f"{user_id}@company.com"}

# --- MAIN LOGIC ---
def sync_user_permissions():
    users = ["ID_01", "ID_02", "ID_03", "ID_04", "ID_05"]
    log.info(f"Starting permission sync for {len(users)} users")

    for user_id in users:
        t_id = str(uuid.uuid4())[:8] 
        try:
            profile = get_user_profile(user_id, t_id)
            if profile is None:
                log.error(f"Sync failed: User {user_id} profile not found", extra={"trace_id": t_id})
                continue
                
            if profile['role'] == "admin":
                log.info(f"Syncing permissions for {user_id}", extra={"trace_id": t_id})
                time.sleep(0.1)
                
        except Exception as e:
            log.critical(f"Unexpected error during sync for {user_id}", exc_info=True, extra={"trace_id": t_id})

    log.info("Process finished!")

if __name__ == "__main__":
    sync_user_permissions()