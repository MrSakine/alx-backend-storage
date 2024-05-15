#!/usr/bin/env python3
""" Redis basic """
from functools import wraps
import typing
import uuid
import redis
from typing import Union, Optional, Callable, Any


def count_calls(method: Callable) -> Callable:
    """
    Count how many times methods of the Cache class are called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper content"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Storing lists"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper content"""
        key = method.__qualname__
        inp = key + ":inputs"
        out = key + ":outputs"
        res = method(self, *args)
        self._redis.rpush(inp, str(args))
        self._redis.rpush(out, res)
        return res
    return wrapper


def replay(store: Callable) -> None:
    """Retrieving lists"""
    key = store.__qualname__
    cache = store.__self__
    client = cache._redis
    inp = key + ":inputs"
    out = key + ":outputs"
    c = client.get(key)
    calls = cache.get_int(c) if c is not None else 0
    inputs = [
        cache.get_str(input)
        for input in client.lrange(inp, 0, -1)
    ]
    outputs = [
        cache.get_str(output)
        for output in client.lrange(out, 0, -1)
    ]
    print(f"{key} was called {calls} times:")
    for i, o in zip(inputs, outputs):
        print(f"{key}(*{i}) -> {o}")


class Cache():
    def __init__(self):
        """Initialize redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """
        Generate a random key using uuid,
        store the input data in Redis using the random key
        and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Reading from Redis and recovering original type"""
        element = self._redis.get(key)
        if not element:
            return None
        elif fn is int:
            return self.get_int(element)
        elif fn is str:
            return self.get_str(element)
        elif callable(fn):
            return fn(element)
        else:
            return element

    def get_str(self, data: bytes) -> str:
        """Converts bytes to string"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """Converts bytes to integers"""
        return int(data)
