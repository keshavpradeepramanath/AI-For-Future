import redis
import json
import hashlib

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def generate_cache_key(jd_text, resume_text):

    combined = jd_text + resume_text

    return hashlib.md5(combined.encode()).hexdigest()


def get_cached_result(key):

    result = redis_client.get(key)

    if result:
        return json.loads(result)

    return None


def store_cached_result(key, data):

    redis_client.set(key, json.dumps(data))