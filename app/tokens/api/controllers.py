from typing import Tuple, Any, List

from fastapi import HTTPException
from jose import jwt, JWTError

from app.config import settings
from .. import models
from . import schemas


async def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, settings.tokens_algorithm)
    except JWTError as exc:
        raise HTTPException(status_code=400, detail=f'JWTError: {str(exc)}')


async def _delete_actual_tokens(user_id: int):
    for expired_token in models.Token.filter(user_id=user_id):
        expired_token.delete()


async def _delete_actual_refresh_tokens(user_id: int):
    for expired_rtoken in models.RefreshToken.filter(user_id=user_id):
        expired_rtoken.delete()


async def _delete_user_tokens(user_id: int):
    await _delete_actual_tokens(user_id)
    await _delete_actual_refresh_tokens(user_id)


async def _create_new_tokens(user_id: int) -> Tuple[models.Token, models.RefreshToken]:
    token = models.Token.create(user_id)
    rtoken = models.RefreshToken.create(user_id)
    return token, rtoken


async def _search_tokens(token: str, kind='token') -> Tuple[Any, List[models.Token]]:
    decoded = await _decode_token(token)
    if kind == 'token':
        results = models.Token.filter(
            user_id=decoded.get('user_id'),
            nonce=decoded.get('nonce'),
        )
    else:
        results = models.RefreshToken.filter(
            user_id=decoded.get('user_id'),
            nonce=decoded.get('nonce'),
        )

    if not results:
        raise HTTPException(status_code=401)

    return decoded, results


async def create_token(payload: schemas.AuthFormSchema) -> schemas.AuthSchema:
    # TODO check if user exists before create tokens

    token, rtoken = await _create_new_tokens(payload.user_id)
    return schemas.AuthSchema.model_validate(
        {
            'user_id': token.user_id,
            'token': token.token,
            'refresh_token': rtoken.token,
            'token_nonce': token.nonce,
            'refresh_token_nonce': rtoken.nonce,
        }
    )


async def get_token(token: str) -> models.Token:
    decoded = await _decode_token(token)
    results = models.Token.filter(
        user_id=decoded.get('user_id'),
        nonce=decoded.get('nonce'),
    )
    if not results:
        raise HTTPException(status_code=401)

    return results[0]


async def refresh_token(token: str) -> models.Token:
    decoded, _ = await _search_tokens(token, kind='refresh')
    await _delete_actual_tokens(decoded.get('user_id'))
    return models.Token.create(decoded.get('user_id'))


async def delete_token(token: str):
    decoded, _ = await _search_tokens(token)
    await _delete_user_tokens(decoded.get('user_id'))
