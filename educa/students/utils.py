import redis
from django.conf import settings


# setting up the Redis connection
def get_redis_connection():
    return redis.Redis(host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=settings.REDIS_DB,
                    decode_responses=True   # ensure responses are strings
                    )
