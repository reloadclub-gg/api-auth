import pytest

from reload_redis import redis_client_instance as cache
from jose.exceptions import JWSError

from app.tests import BaseTest
from app.config import settings
from .. import models


class TestToken(BaseTest):
    def test_create(self):
        model = models.Token.create(user_id=1)
        assert model.token is not None
        assert model.nonce is not None
        assert model.user_id is not None
        model_hash = cache.hgetall(model.cache_key)
        assert model_hash is not None
        assert model.token == model_hash.get('token')
        assert model.nonce == int(model_hash.get('nonce'))
        assert model.user_id == int(model_hash.get('user_id'))

    def test_create_invalid_token(self):
        settings.tokens_algorithm = 'invalid'
        with pytest.raises(JWSError):
            models.Token.create(user_id=1)
        settings.tokens_algorithm = 'HS256'


class TestRefreshToken(BaseTest):
    def test_create(self):
        model = models.RefreshToken.create(user_id=1)
        assert model.token is not None
        model_hash = cache.hgetall(model.cache_key)
        assert model_hash is not None
        assert model.token == model_hash.get('token')
