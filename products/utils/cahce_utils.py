# utils/cache_utils.py
from django.core.cache import cache

def clear_cache_by_prefix(prefix: str):
    """
    Deletes all cache keys starting with a given prefix.
    Works only if your cache backend supports .keys() (like Redis).
    """
    try:
        # Get all cache keys (works in Redis backend)
        keys = cache.keys(f"{prefix}*")
        if keys:
            cache.delete_many(keys)
            print(f"✅ Cleared {len(keys)} cache keys starting with '{prefix}'")
    except Exception as e:
        print(f"⚠️ Cache clearing failed: {e}")
