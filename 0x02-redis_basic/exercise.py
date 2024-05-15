#!/usr/bin/env python3
""" Redis basic """
import typing
import uuid
import redis
from typing import Union, Optional, Callable, Any


class Cache():
    def __init__(self):
        """Initialize redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
