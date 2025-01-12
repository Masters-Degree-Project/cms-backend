import os
import redis

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
) 

def add_to_queue(task_name, *args, **kwargs):
    redis_client.rpush(task_name, *args, **kwargs)