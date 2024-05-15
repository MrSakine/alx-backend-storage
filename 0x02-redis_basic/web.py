#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
from functools import wraps
import requests
import redis


def cache_page(expiration: int):
    """ Page cache decorator """
    def decorator(func):
        """ Wrapper header """
        @wraps(func)
        def wrapper(url: str):
            """ Wrapper body """
            client = redis.Redis()
            cache_key = f"page:{url}"
            count_key = f"count:{url}"
            client.incr(count_key)
            cached_result = client.get(cache_key)
            if cached_result:
                return cached_result
            result = func(url)
            client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """expiring web cache and tracker"""
    return requests.get(url).text
