import time
import logging

from app import extensions
from app.core.logger import logger



ROLE_LIMITS = {
    "free": {"capacity": 5, "refill_rate": 5/60},  # 5 requests per minute
    "paid": {"capacity": 10, "refill_rate": 10/60}  # 10 requests per minute
}


TOKEN_BUCKET_LUA = """ 

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now =tonumber(ARGV[3])

local bucket = redis.call("HMGET", key, "tokens", "last_refill")

local tokens = tonumber(bucket[1])
local last_refill = tonumber(bucket[2])

if tokens == nil then
   tokens = capacity
   last_refill = now
end

local elapsed = now - last_refill
local refill = elapsed * refill_rate
tokens = math.min(capacity, tokens + refill)

if tokens < 1 then
   redis.call("HMSET", key,
   "tokens", tokens,
   "last_refill", now)
   redis.call("EXPIRE", key, 3600)
   return {0, tokens}
end

tokens = tokens -1

redis.call("HMSET", key,
    "tokens", tokens,
    "last_refill", now)

redis.call("EXPIRE", key, 3600)

return {1, tokens}
"""

class RateLimiterService:

    def __init__(self):
        # register script lazily because redis_client may be initialized
        # after this service is instantiated (app factory pattern)
        self.lua_script = None



    def allow_request(self, user_id: str, role: str = "free"):
        # lazy-register the LUA script if redis client is available now
        if not self.lua_script:
            redis_client = extensions.redis_client.redis_client
            if redis_client:
                try:
                    self.lua_script = redis_client.register_script(TOKEN_BUCKET_LUA)
                except Exception as e:
                    logger.error(f"Failed to register lua script: {e}")
                    return True, 0, 0
            else:
                # Redis not configured yet — allow requests instead of blocking
                return True, 0, 0

        limits = ROLE_LIMITS.get(role, ROLE_LIMITS["free"])
        capacity = limits["capacity"]
        refill_rate = limits["refill_rate"]

        try:
            result = self.lua_script(
                keys=[f"rate_limit:{user_id}"],
                args=[capacity, refill_rate, int(time.time())]
            )

            allowed = bool(int(result[0]))
            remaining = int(float(result[1]))

            logger.info(f"RateLimiter: user={user_id} role={role} allowed={allowed} remaining={remaining} capacity={capacity}")

            return allowed, remaining, capacity
        
        except Exception as e:
            logger.exception("Redis failure")
            return True, 0, capacity
