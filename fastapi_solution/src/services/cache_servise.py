from typing import Any

from .redis_service import BaseStorage
from .my_types import CacheKeyChoices


class CacheService:
    def __init__(self, storage: BaseStorage = None,):
        self.storage = storage
        self.timeout: int = 60 * 60 * 24 * 1

    def set_key(
        self,
        key: CacheKeyChoices | str,
        version: str | int | None
    ):
        return f"{key}:{version}" if version is not None else key

    def cache_get(self, key: CacheKeyChoices | str, version: str | int | None):
        key = self.set_key(key, version)
        return self.storage.retrieve_state(key)

    def cache_set(
        self,
        key: CacheKeyChoices | str,
        version: str | int | None,
        value: Any,
        timeout: int = None
    ):

        key = self.set_key(key, version)
        return self.storage.save_state(
            key, value, ex=timeout or self.timeout
        )

    def cache_delete(self, key: str, version: str | int | None):
        key = self.set_key(key, version)
        self.storage.delete_state(key)
