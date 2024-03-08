from fastapi import APIRouter, Request
from fastapi.security import OAuth2PasswordBearer

from . import controllers

router = APIRouter(tags=['auth'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/signin/start')
async def signin_start():
    return await controllers.signin_start()


@router.get('/signin/complete')
async def signin_complete(request: Request):
    payload = dict(request.query_params)
    return await controllers.signin_complete(payload)
