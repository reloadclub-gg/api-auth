from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from . import controllers, schemas

router = APIRouter(tags=['tokens'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/')
async def detail(token: Annotated[str, Depends(oauth2_scheme)]) -> schemas.TokenSchema:
    return await controllers.get_token(token)


@router.post('/')
async def create(payload: schemas.AuthFormSchema) -> schemas.AuthSchema:
    return await controllers.create_token(payload)


@router.patch('/')
async def refresh(
    rtoken: Annotated[str, Depends(oauth2_scheme)]
) -> schemas.TokenNonceSchema:
    return await controllers.refresh_token(rtoken)


@router.delete('/')
async def delete(token: Annotated[str, Depends(oauth2_scheme)]):
    return await controllers.delete_token(token)
