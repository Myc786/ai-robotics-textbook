import asyncio
import time
from typing import Any, Dict, Optional
from collections import OrderedDict


class SimpleCache:
    """
    A simple in-memory cache with TTL (Time To Live) and LRU (Least Recently Used) eviction.
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):  # 5 minutes default TTL
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache = OrderedDict()
        self._ttl = {}  # Store expiration times

    def _is_expired(self, key: str) -> bool:
        """Check if a cache entry has expired."""
        if key not in self._ttl:
            return True
        return time.time() > self._ttl[key]

    def get(self, key: str) -> Optional[Any]:
        """Get a value from the cache."""
        if key not in self._cache or self._is_expired(key):
            if key in self._cache:
                # Remove expired entry
                del self._cache[key]
                del self._ttl[key]
            return None

        # Move to end to mark as recently used
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the cache with optional TTL."""
        if ttl is None:
            ttl = self.default_ttl

        # Remove expired entries if needed
        if key in self._cache:
            del self._cache[key]
            del self._ttl[key]

        # Evict oldest entries if cache is full
        while len(self._cache) >= self.max_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            if oldest_key in self._ttl:
                del self._ttl[oldest_key]

        # Add new entry
        self._cache[key] = value
        self._ttl[key] = time.time() + ttl

    def delete(self, key: str) -> bool:
        """Delete a value from the cache."""
        if key in self._cache:
            del self._cache[key]
            if key in self._ttl:
                del self._ttl[key]
            return True
        return False

    def clear(self) -> None:
        """Clear all entries from the cache."""
        self._cache.clear()
        self._ttl.clear()

    def size(self) -> int:
        """Get the current size of the cache."""
        # Clean up expired entries first
        expired_keys = [key for key in self._cache if self._is_expired(key)]
        for key in expired_keys:
            del self._cache[key]
            del self._ttl[key]
        
        return len(self._cache)


class CachingService:
    """
    Service to handle caching of frequently accessed content and query results.
    """
    
    def __init__(self):
        self.cache = SimpleCache(max_size=10000, default_ttl=600)  # 10 minutes for most items
        self.query_cache = SimpleCache(max_size=5000, default_ttl=300)  # 5 minutes for query results
        self.content_cache = SimpleCache(max_size=2000, default_ttl=900)  # 15 minutes for content

    async def get_cached_query_result(self, query_hash: str) -> Optional[Dict[str, Any]]:
        """Get a cached query result."""
        return self.query_cache.get(query_hash)

    async def cache_query_result(self, query_hash: str, result: Dict[str, Any], ttl: Optional[int] = None) -> None:
        """Cache a query result."""
        self.query_cache.set(query_hash, result, ttl)

    async def get_cached_content(self, content_id: str) -> Optional[str]:
        """Get cached content."""
        return self.content_cache.get(content_id)

    async def cache_content(self, content_id: str, content: str, ttl: Optional[int] = None) -> None:
        """Cache content."""
        self.content_cache.set(content_id, content, ttl)

    async def invalidate_content_cache(self, content_id: str) -> bool:
        """Invalidate a specific content cache entry."""
        return self.content_cache.delete(content_id)

    async def get_cached_embedding(self, text_hash: str) -> Optional[list]:
        """Get a cached embedding."""
        return self.cache.get(f"embedding:{text_hash}")

    async def cache_embedding(self, text_hash: str, embedding: list, ttl: Optional[int] = None) -> None:
        """Cache an embedding."""
        self.cache.set(f"embedding:{text_hash}", embedding, ttl)

    async def invalidate_cache(self, key: str) -> bool:
        """Invalidate a specific cache entry."""
        return self.cache.delete(key)

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "total_cache_size": self.cache.size(),
            "query_cache_size": self.query_cache.size(),
            "content_cache_size": self.content_cache.size()
        }