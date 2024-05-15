#!/usr/bin/env python3
""" Writing strings to Redis """
import uuid
import redis

class Cache():
    def __init__(self):
        """Initialize redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()
        
    def store(self, data: any) -> str:
        """
        Generate a random key using uuid,
        store the input data in Redis using the random key
        and return the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
