from functools import wraps
from collections import OrderedDict


def cache_decorator(cache_limit=0):
    if not isinstance(cache_limit, int) or cache_limit < 0:
        raise ValueError("cache_limit must be a non-negative integer.")

    def decorator(func):
        cache = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, frozenset(kwargs.items()))

            if cache_key in cache:
                return cache[cache_key]

            result = func(*args, **kwargs)

            if cache_limit > 0:
                if len(cache) >= cache_limit:
                    cache.popitem(last=False)
                cache[cache_key] = result

            return result

        wrapper.cache = cache

        return wrapper

    return decorator
