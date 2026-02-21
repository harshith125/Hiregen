from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from typing import Any
from services.analytics import (
    calculate_avg_package_per_branch,
    calculate_skill_roi,
    get_hiring_trends
)

router = APIRouter()

# Simple In-Memory Cache Implementation
# Caches endpoint results to minimize pandas processing delays for the frontend.
class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):
        self._cache = {}
        self.ttl = timedelta(seconds=ttl_seconds)

    def get(self, key: str) -> Any:
        if key in self._cache:
            item, timestamp = self._cache[key]
            if datetime.now() - timestamp < self.ttl:
                return item
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        self._cache[key] = (value, datetime.now())

# Set cache TTL to 5 minutes
analytics_cache = SimpleCache(ttl_seconds=300)

@router.get("/avg-package")
async def get_avg_package(year: int = Query(..., description="Year to analyze")):
    cache_key = f"avg-package-{year}"
    cached = analytics_cache.get(cache_key)
    if cached is not None:
        return cached

    result = await calculate_avg_package_per_branch(year)
    analytics_cache.set(cache_key, result)
    return result

@router.get("/skill-roi")
async def get_skill_roi():
    cache_key = "skill-roi"
    cached = analytics_cache.get(cache_key)
    if cached is not None:
        return cached

    result = await calculate_skill_roi()
    analytics_cache.set(cache_key, result)
    return result

@router.get("/hiring-trends")
async def get_trends():
    cache_key = "hiring-trends"
    cached = analytics_cache.get(cache_key)
    if cached is not None:
        return cached

    result = await get_hiring_trends()
    analytics_cache.set(cache_key, result)
    return result
