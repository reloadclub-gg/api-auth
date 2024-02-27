from fastapi import FastAPI

from .models import AuthModel, ModelCreationForm

application = FastAPI()


@application.get('/')
async def detail(token: str):
    return AuthModel.filter(token=token)


@application.post('/')
async def create(payload: ModelCreationForm) -> AuthModel:
    return AuthModel.create(**payload.model_dump())
