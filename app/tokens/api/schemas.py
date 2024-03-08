from pydantic import BaseModel


class TokenSchema(BaseModel):
    steamid: str
    token: str


class TokenNonceSchema(BaseModel):
    steamid: str
    token: str
    nonce: int


class AuthSchema(BaseModel):
    steamid: str
    token: str
    refresh_token: str
    token_nonce: int
    refresh_token_nonce: int


class AuthFormSchema(BaseModel):
    steamid: str
