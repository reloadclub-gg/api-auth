import pytest
from reload_redis import redis_client_instance as cache


class BaseTest:
    @pytest.fixture(autouse=True)
    def clear_cache(self):
        yield
        cache.flushdb()
