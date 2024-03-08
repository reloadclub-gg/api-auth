import pytest

from reload_redis import redis_client_instance as cache
from jose.exceptions import JWSError

from app.tests import BaseTest
from app.config import settings
from .. import models


class TestToken(BaseTest):
    def test_create(self):
        model = models.Token.create(steamid='steamid')
        assert model.token is not None
        assert model.nonce is not None
        assert model.steamid is not None
        model_hash = cache.hgetall(model.cache_key)
        assert model_hash is not None
        assert model.token == model_hash.get('token')
        assert model.nonce == int(model_hash.get('nonce'))
        assert model.steamid == model_hash.get('steamid')

    def test_create_invalid_token(self):
        settings.tokens_algorithm = 'invalid'
        with pytest.raises(JWSError):
            models.Token.create(steamid='steamid')
        settings.tokens_algorithm = 'HS256'


class TestRefreshToken(BaseTest):
    def test_create(self):
        model = models.RefreshToken.create(steamid='steamid')
        assert model.token is not None
        model_hash = cache.hgetall(model.cache_key)
        assert model_hash is not None
        assert model.token == model_hash.get('token')
