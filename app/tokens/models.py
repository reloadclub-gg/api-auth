from datetime import datetime

from reload_redis import redis_client_instance as cache, models
from jose import jwt, JWTError
from jose.exceptions import JWSError

from app.config import settings


class BaseTokenModel(models.RedisBaseModel):
    class ConfigDict:
        CACHE_NAME = 'token'
        EXPIRE_TIME = 7200  # 2h
        NONCE_ENCRYPT = 8

    user_id: int
    token: str
    nonce: int

    @classmethod
    def create(cls, user_id: int, **kwargs):
        now = int(datetime.now().timestamp())
        nonce = now * cls.ConfigDict.NONCE_ENCRYPT

        jwt_data = {'user_id': user_id, 'nonce': nonce}
        try:
            jwt_token = jwt.encode(
                jwt_data,
                settings.secret_key,
                settings.tokens_algorithm,
            )
        except (JWTError, JWSError) as exc:
            raise exc

        model = super().create(user_id=user_id, token=jwt_token, nonce=nonce, **kwargs)
        cache.expire(model.cache_key, BaseTokenModel.ConfigDict.EXPIRE_TIME)
        return model


class Token(BaseTokenModel):
    pass


class RefreshToken(BaseTokenModel):
    class ConfigDict:
        CACHE_NAME = 'rtoken'
        EXPIRE_TIME = 604800  # 7d
        NONCE_ENCRYPT = 16
