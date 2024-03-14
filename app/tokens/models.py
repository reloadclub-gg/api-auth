from datetime import datetime

from jose import JWTError, jwt
from jose.exceptions import JWSError
from reload_redis import models
from reload_redis import redis_client_instance as cache

from app.config import settings


class BaseTokenModel(models.RedisBaseModel):
    class ConfigDict:
        CACHE_NAME = 'token'
        EXPIRE_TIME = 7200  # 2h
        NONCE_ENCRYPT = 8

    steamid: str
    token: str
    nonce: int

    @classmethod
    def create(cls, steamid: str, **kwargs):
        now = int(datetime.now().timestamp())
        nonce = now * cls.ConfigDict.NONCE_ENCRYPT

        jwt_data = {'steamid': steamid, 'nonce': nonce}
        try:
            jwt_token = jwt.encode(
                jwt_data,
                settings.secret_key,
                settings.tokens_algorithm,
            )
        except (JWTError, JWSError) as exc:
            raise exc

        model = super().create(steamid=steamid, token=jwt_token, nonce=nonce, **kwargs)
        cache.expire(model.cache_key, BaseTokenModel.ConfigDict.EXPIRE_TIME)
        return model


class Token(BaseTokenModel):
    pass


class RefreshToken(BaseTokenModel):
    class ConfigDict:
        CACHE_NAME = 'rtoken'
        EXPIRE_TIME = 604800  # 7d
        NONCE_ENCRYPT = 16
