import uuid
import time
import random
from logger_config import log

def fetch_user_data(user_id, trace_id):
    """Simulates fetching raw data from a source."""
    # DEBUG: Show the 'behind the scenes' raw data
    raw_response = {"id": user_id, "status": 200, "payload": {"val": random.randint(10, 100)}}
    
    # 🧪 DEMONSTRATING DEBUG:
    log.debug(f"RAW API RESPONSE: {raw_response}", extra={"trace_id": trace_id})
    
    # Simulating a logic for WARNING
    if user_id == "USER_05" or user_id == "USER_15":
        log.warning(f"Connection unstable for {user_id}. Using cached headers.", extra={"trace_id": trace_id})
        
    # Simulating the ERROR scenario
    if user_id == "USER_07" or user_id == "USER_17":
        return {"id": user_id, "broken_payload": None} # Missing 'payload' key
        
    return raw_response

def process_request(user_id):
    t_id = str(uuid.uuid4())[:8]
    
    # INFO: The Milestone
    log.info(f"Processing request for {user_id}", extra={"trace_id": t_id})

    try:
        data = fetch_user_data(user_id, t_id)
        
        # This line will fail for USER_07
        result = data["payload"]["val"] * 2 
        
        log.info(f"Calculation complete for {user_id}: Result={result}", extra={"trace_id": t_id})

    except KeyError:
        # ERROR: A failure that we handled
        log.error(f"Failed to find 'payload' in API response for {user_id}", exc_info=True, extra={"trace_id": t_id})
    except Exception:
        # CRITICAL: Something very bad (like the server running out of memory)
        log.critical("SYSTEM CRITICAL: Unexpected failure!", exc_info=True, extra={"trace_id": t_id})

if __name__ == "__main__":
    # --- STEP 1: Define which batch to run ---
    # Batch 1: 1-10 (Dev Mode / DEBUG)
    # Batch 2: 11-20 (Prod Mode / INFO)
    batch_number = 2

    if batch_number == 1:
        start_id = 1 
        end_id = 11 
    elif batch_number == 2:
        start_id = 11 
        end_id = 21 
    else:
        raise ValueError(f"Invalid batch number: {batch_number}")

    # --- STEP 2: Generate the list dynamically ---
    # This is called List Comprehension. 
    # {i:02d} means: take the number, make it 2 digits, and pad with a zero if needed.
    users = [f"USER_{i:02d}" for i in range(start_id, end_id)]

    print(f"--- Running Simulation for {users[0]} to {users[-1]} ---")

    for user in users:
        process_request(user)
        # Small delay to make the terminal look like it's "working"
        time.sleep(0.1)