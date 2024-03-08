from fastapi import FastAPI

from .api import endpoints as main_endpoints
from .tokens.api import endpoints as tokens_endpoints


application = FastAPI()
application.include_router(main_endpoints.router)
application.include_router(tokens_endpoints.router)
