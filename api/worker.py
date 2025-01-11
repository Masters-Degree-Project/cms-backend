import time
from .tasks import process_content_language
from .queue import redis_client

def start_worker():
    print("Worker started...")
    while True:
        try:
            # Queue'dan iş al
            result = redis_client.brpop('content_language_queue', timeout=1)
            if result:
                content_language_id = result[1]
                process_content_language(int(content_language_id))
        except Exception as e:
            print(f"Error processing task: {e}")
        
        time.sleep(1)

if __name__ == '__main__':
    start_worker() 