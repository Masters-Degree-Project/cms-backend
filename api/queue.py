import redis

from app.settings import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
) 

def add_to_queue(task_name, *args, **kwargs):
    redis_client.rpush(task_name, *args, **kwargs)