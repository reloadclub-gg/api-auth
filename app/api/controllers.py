from typing import Dict, Any

from fastapi import HTTPException
from fastapi.responses import RedirectResponse
import urllib.parse
import requests

from app.config import settings
from app.tokens.api.schemas import AuthSchema
from app.tokens.api.controllers import _create_new_tokens
from app.sessions.models import Session


async def _get_request_openid_params() -> Dict[str, Any]:
    return {
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.mode': 'checkid_setup',
        'openid.return_to': f'{settings.app_base_url}/signin/complete',
        'openid.realm': settings.app_base_url,
        'openid.identity': 'http://specs.openid.net/auth/2.0/identifier_select',
        'openid.claimed_id': 'http://specs.openid.net/auth/2.0/identifier_select',
    }


async def _is_auth_valid(payload: Dict[str, Any]) -> str:
    payload['openid.mode'] = 'check_authentication'
    res = requests.post(settings.steam_openid_url, data=payload)
    return 'is_valid:true' in res.text


async def _steamid64_to_hex(steamid64: str) -> str:
    steamid_hex = hex(int(steamid64))
    if steamid_hex.startswith('0x'):
        steamid_hex = steamid_hex[2:]

    return steamid_hex


async def _get_steamid_hex(payload: Dict[str, Any]) -> Session:
    steamid64 = payload.get(settings.steam_openid_lookup_field).split('/')[-1]
    return await _steamid64_to_hex(steamid64)


async def signin_start():
    params = await _get_request_openid_params()
    parsed_params = urllib.parse.urlencode(params)
    redirect_url = f'{settings.steam_openid_url}?{parsed_params}'
    return RedirectResponse(redirect_url)


async def signin_complete(payload: Dict[str, Any]):
    if not _is_auth_valid(payload):
        raise HTTPException(status_code=400)

    steamid = await _get_steamid_hex(payload)

    # TODO if not user return 401 'not registered'

    token, rtoken = await _create_new_tokens(steamid)
    Session.create(steamid=steamid)
    return AuthSchema.model_validate(
        {
            'steamid': steamid,
            'token': token.token,
            'refresh_token': rtoken.token,
            'token_nonce': token.nonce,
            'refresh_token_nonce': rtoken.nonce,
        }
    )
