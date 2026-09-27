import json
import time
from typing import Optional, Any
from api.config import settings

_redis_client = None
_redis_available = False

# Local in-memory cache fallback for $0 development/testing
_local_cache = {}
_cache_stats = {"hits": 0, "misses": 0}

def get_redis():
    global _redis_client, _redis_available
    if _redis_client is not None:
        return _redis_client
    try:
        import redis
        client = redis.Redis.from_url(settings.REDIS_URL, socket_timeout=0.5)
        client.ping()
        _redis_client = client
        _redis_available = True
        print("[OK] Connected to Redis cache")
        return _redis_client
    except Exception:
        _redis_available = False
        return None

# Attempt non-blocking connection on import
get_redis()

def cache_get(key: str) -> Optional[Any]:
    global _cache_stats
    r = get_redis()
    if r:
        try:
            val = r.get(key)
            if val:
                _cache_stats["hits"] += 1
                return json.loads(val.decode("utf-8"))
        except Exception:
            pass

    # Check local cache
    entry = _local_cache.get(key)
    if entry:
        val, expiry = entry
        if expiry is None or expiry > time.time():
            _cache_stats["hits"] += 1
            return val
        else:
            del _local_cache[key]

    _cache_stats["misses"] += 1
    return None

def cache_set(key: str, value: Any, ttl_seconds: int = 300) -> None:
    r = get_redis()
    if r:
        try:
            r.setex(key, ttl_seconds, json.dumps(value))
            return
        except Exception:
            pass

    # Local fallback
    _local_cache[key] = (value, time.time() + ttl_seconds)

def get_cache_stats() -> dict:
    total = _cache_stats["hits"] + _cache_stats["misses"]
    hit_rate = round((_cache_stats["hits"] / total) * 100, 2) if total > 0 else 0.0
    return {
        "hits": _cache_stats["hits"],
        "misses": _cache_stats["misses"],
        "hit_rate_pct": hit_rate,
        "backend": "Redis" if _redis_available else "Local In-Memory Cache",
    }
