from pydantic import BaseModel


class TokenSchema(BaseModel):
    user_id: int
    token: str


class TokenNonceSchema(BaseModel):
    user_id: int
    token: str
    nonce: int


class AuthSchema(BaseModel):
    user_id: int
    token: str
    refresh_token: str
    token_nonce: int
    refresh_token_nonce: int


class AuthFormSchema(BaseModel):
    user_id: int
