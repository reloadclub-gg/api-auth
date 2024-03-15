from pydantic import BaseModel


class TokenSchema(BaseModel):
    steamid: str
    token: str
    expire_at: float


class TokenNonceSchema(BaseModel):
    steamid: str
    token: str
    nonce: float
    expire_at: float


class AuthSchema(BaseModel):
    steamid: str
    token: str
    token_nonce: float
    token_expire_at: float
    refresh_token: str
    refresh_token_nonce: float
    refresh_token_expire_at: float


class AuthFormSchema(BaseModel):
    steamid: str
