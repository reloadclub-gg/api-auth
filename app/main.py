from fastapi import FastAPI

from .tokens.api import endpoints as tokens_endpoints


application = FastAPI()
application.include_router(tokens_endpoints.router)
