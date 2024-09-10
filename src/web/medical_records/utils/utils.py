from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist


def get_cached_data(cache_key, query_func, timeout=60*15):
    """
    Utility function to handle caching for both single objects and querysets.

    Arguments:
    - cache_key: The key to use for caching.
    - query_func: A function that returns the data if not cached (e.g., a query).
    - timeout: Cache timeout in seconds (default 15 minutes).

    Returns:
    - Cached data or the result of the query if not in cache.
    """
    data = cache.get(cache_key)

    if not data:
        try:
            data = query_func()
            cache.set(cache_key, data, timeout)
        except ObjectDoesNotExist:
            data = None

    return data
