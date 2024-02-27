from pydantic import BaseModel
from reload_redis.models import RedisBaseModel


class AuthModel(RedisBaseModel):
    class ConfigDict:
        CACHE_NAME = 'auth'

    user_id: int
    token: str


class ModelCreationForm(BaseModel):
    user_id: int
