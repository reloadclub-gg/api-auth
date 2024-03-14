from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.config import settings

from . import controllers, schemas

router = APIRouter(prefix='/tokens', tags=['tokens'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/')
async def detail(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.TokenSchema:
    return await controllers.get_token(token)


@router.post('/')
async def create(payload: schemas.AuthFormSchema) -> schemas.AuthSchema:
    if settings.debug:
        return await controllers.create_token(payload)

    return HTTPException(status_code=404)


@router.patch('/')
async def refresh(rtoken: Annotated[str, Depends(oauth2_scheme)]) -> schemas.TokenNonceSchema:
    return await controllers.refresh_token(rtoken)


@router.delete('/')
async def delete(token: Annotated[str, Depends(oauth2_scheme)]):
    return await controllers.delete_token(token)
