from datetime import datetime

from reload_redis import models
from reload_redis import redis_client_instance as cache


class Session(models.RedisBaseModel):
    class ConfigDict:
        CACHE_NAME = 'session'
        EXPIRE_TIME = 15  # 15s

    steamid: str
    last_timestamp: str

    @classmethod
    def create(cls, **kwargs):
        model = super().create(last_timestamp=str(datetime.now().timestamp), **kwargs)
        cache.expire(model.cache_key, Session.ConfigDict.EXPIRE_TIME)
        return model
