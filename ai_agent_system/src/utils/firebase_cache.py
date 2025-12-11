"""Firestore-based caching implementation to replace Redis."""
import os
import json
from typing import Optional, Any
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import firestore
from functools import lru_cache

from src.config.logging_config import get_logger

logger = get_logger(module=__name__)


class FirestoreCache:
    """Firestore-based cache implementation."""
    
    _instance: Optional['FirestoreCache'] = None
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firestore client."""
        if not self._initialized:
            try:
                # Get Firestore client (Firebase app should already be initialized)
                self.db = firestore.client()
                self.cache_collection = self.db.collection('cache')
                logger.info("Firestore cache initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Firestore cache: {e}")
                self.db = None
                self.cache_collection = None
            
            self.__class__._initialized = True
    
    async def get(self, key: str) -> Optional[str]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        if not self.cache_collection:
            return None
        
        try:
            doc_ref = self.cache_collection.document(key)
            doc = doc_ref.get()
            
            if not doc.exists:
                logger.debug(f"Cache miss: {key}")
                return None
            
            data = doc.to_dict()
            
            # Check expiration
            expires_at = data.get('expires_at')
            if expires_at and expires_at < datetime.utcnow():
                # Delete expired entry
                await self.delete(key)
                logger.debug(f"Cache expired: {key}")
                return None
            
            logger.debug(f"Cache hit: {key}")
            return data.get('value')
            
        except Exception as e:
            logger.error(f"Error getting cache: {e}")
            return None
    
    async def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None for no expiration)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.cache_collection:
            return False
        
        try:
            expires_at = None
            if ttl:
                expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            
            doc_ref = self.cache_collection.document(key)
            doc_ref.set({
                'value': value,
                'created_at': datetime.utcnow(),
                'expires_at': expires_at,
            })
            
            logger.debug(f"Cache set: {key} (TTL: {ttl})")
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        if not self.cache_collection:
            return False
        
        try:
            doc_ref = self.cache_collection.document(key)
            doc_ref.delete()
            logger.debug(f"Cache deleted: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")
            return False
    
    async def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists and not expired, False otherwise
        """
        value = await self.get(key)
        return value is not None
    
    async def clear(self) -> bool:
        """
        Clear all cache entries.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.cache_collection:
            return False
        
        try:
            # Delete all documents in cache collection
            docs = self.cache_collection.stream()
            batch = self.db.batch()
            count = 0
            
            for doc in docs:
                batch.delete(doc.reference)
                count += 1
                
                # Commit in batches of 500 (Firestore limit)
                if count % 500 == 0:
                    batch.commit()
                    batch = self.db.batch()
            
            # Commit remaining
            if count % 500 != 0:
                batch.commit()
            
            logger.info(f"Cache cleared: {count} entries deleted")
            return True
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return False
    
    async def get_json(self, key: str) -> Optional[Any]:
        """
        Get JSON value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Parsed JSON value if found, None otherwise
        """
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in cache: {key}")
                return None
        return None
    
    async def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set JSON value in cache.
        
        Args:
            key: Cache key
            value: Value to serialize and cache
            ttl: Time to live in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            json_value = json.dumps(value)
            return await self.set(key, json_value, ttl)
        except (TypeError, ValueError) as e:
            logger.error(f"Error serializing JSON: {e}")
            return False


@lru_cache()
def get_firestore_cache() -> FirestoreCache:
    """Get Firestore cache singleton instance."""
    return FirestoreCache()
