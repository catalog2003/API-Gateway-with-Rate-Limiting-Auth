import os
import sys
from pathlib import Path

# project app path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

os.environ.setdefault('REDIS_HOST', 'localhost')
os.environ.setdefault('REDIS_PORT', '6379')

import redis

# inject a redis client into app.extensions.redis_client
from app.extensions import redis_client as redis_ext
r = redis.Redis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']), decode_responses=True)
redis_ext.redis_client = r

from app.services.rate_limiter_service import RateLimiterService

rl = RateLimiterService()
user = 'testuser'
for i in range(1, 8):
    allowed, rem, cap = rl.allow_request(user, 'free')
    print(i, allowed, rem, cap)
