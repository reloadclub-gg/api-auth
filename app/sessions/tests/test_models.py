from reload_redis import redis_client_instance as cache

from app.tests import BaseTest
from .. import models


class TestSession(BaseTest):
    def test_create(self):
        model = models.Session.create(steamid='steamid')
        assert model.steamid is not None
        assert model.last_timestamp is not None
        model_hash = cache.hgetall(model.cache_key)
        assert model_hash is not None
        assert model.steamid == model_hash.get('steamid')
        assert model.last_timestamp == model_hash.get('last_timestamp')
