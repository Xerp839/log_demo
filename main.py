import uuid
import time
import random
from logger_config import log

def fetch_user_balance(user_id, trace_id):
    """Simulates an API call to a balance service."""
    # Simulating a "Warning" scenario for specific users (Slow API)
    if user_id in ["USER_08", "USER_09"]:
        log.warning(f"Latency detected for {user_id}. API took 2.5s", extra={"trace_id": trace_id})
        time.sleep(1) # Simulate delay
        
    # THE ERROR TRAP: User 07 triggers a 'Website Schema Change' simulation
    if user_id == "USER_07":
        # We simulate a case where the API returns a different format than expected
        return {"id": user_id, "amount_str": "ERROR_VALUE"} # Should be an integer
    
    return {"id": user_id, "amount": random.randint(50, 500)}

def process_transaction(user_id):
    t_id = str(uuid.uuid4())[:8] # The Trace ID 'Anchor'
    
    log.info(f"START: Processing transaction for {user_id}", extra={"trace_id": t_id})
    
    try:
        # Step 1: Fetch data
        data = fetch_user_balance(user_id, t_id)
        
        # Step 2: Critical Logic (This is where the 'Data Schema' error will happen)
        # We expect 'amount' to be an integer. USER_07 doesn't have 'amount'.
        final_balance = data["amount"] + 10 
        
        log.info(f"SUCCESS: {user_id} balance updated to {final_balance}", extra={"trace_id": t_id})

    except KeyError as e:
        # This pinpoints exactly WHAT happened (Missing key) and WHY (Schema change)
        log.error(
            f"DATA MISMATCH: Expected key 'amount' not found for {user_id}. "
            f"Is the target API schema changed?", 
            exc_info=True, # This adds the full Traceback (the 'Where')
            extra={"trace_id": t_id}
        )
    except Exception as e:
        log.critical(f"UNHANDLED SYSTEM ERROR for {user_id}", exc_info=True, extra={"trace_id": t_id})

if __name__ == "__main__":
    users = [f"USER_{str(i).zfill(2)}" for i in range(1, 11)]
    
    print(f"--- Starting Production Simulation for {len(users)} Users ---\n")
    for user in users:
        process_transaction(user)
        time.sleep(0.1) # Small gap for readability
    print(f"\n--- Simulation Complete. Check logs/ folder! ---")