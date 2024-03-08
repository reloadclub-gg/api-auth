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


async def _delete_actual_tokens(steamid: str):
    for expired_token in models.Token.filter(steamid=steamid):
        expired_token.delete()


async def _delete_actual_refresh_tokens(steamid: str):
    for expired_rtoken in models.RefreshToken.filter(steamid=steamid):
        expired_rtoken.delete()


async def _delete_user_tokens(steamid: str):
    await _delete_actual_tokens(steamid)
    await _delete_actual_refresh_tokens(steamid)


async def _search_tokens(token: str, kind='token') -> Tuple[Any, List[models.Token]]:
    decoded = await _decode_token(token)
    if kind == 'token':
        results = models.Token.filter(
            steamid=decoded.get('steamid'),
            nonce=decoded.get('nonce'),
        )
    else:
        results = models.RefreshToken.filter(
            steamid=decoded.get('steamid'),
            nonce=decoded.get('nonce'),
        )

    if not results:
        raise HTTPException(status_code=401)

    return decoded, results


async def _create_new_tokens(steamid: str) -> Tuple[models.Token, models.RefreshToken]:
    _delete_user_tokens(steamid)
    token = models.Token.create(steamid)
    rtoken = models.RefreshToken.create(steamid)
    return token, rtoken


async def create_token(payload: schemas.AuthFormSchema) -> schemas.AuthSchema:
    # TODO check if user exists before create tokens

    token, rtoken = await _create_new_tokens(payload.steamid)
    return schemas.AuthSchema.model_validate(
        {
            'steamid': token.steamid,
            'token': token.token,
            'refresh_token': rtoken.token,
            'token_nonce': token.nonce,
            'refresh_token_nonce': rtoken.nonce,
        }
    )


async def get_token(token: str) -> models.Token:
    decoded = await _decode_token(token)
    results = models.Token.filter(
        steamid=decoded.get('steamid'),
        nonce=decoded.get('nonce'),
    )
    if not results:
        raise HTTPException(status_code=401)

    return results[0]


async def refresh_token(token: str) -> models.Token:
    decoded, _ = await _search_tokens(token, kind='refresh')
    await _delete_actual_tokens(decoded.get('steamid'))
    return models.Token.create(decoded.get('steamid'))


async def delete_token(token: str):
    decoded, _ = await _search_tokens(token)
    await _delete_user_tokens(decoded.get('steamid'))
