import time
from .tasks import process_prompt_history
from .queue import redis_client

def start_worker():
    print("Worker started...")
    while True:
        try:
            result = redis_client.brpop('prompt_queue', timeout=1)
            if result:
                prompt_history_id = result[1]
                process_prompt_history(int(prompt_history_id))
        except Exception as e:
            print(f"Error processing task: {e}")
        
        time.sleep(1)

if __name__ == '__main__':
    start_worker() 