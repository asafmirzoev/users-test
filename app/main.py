from fastapi import FastAPI

from app.core.Environment import get_environment_variables
from app.metadata.Tags import Tags
from app.models.BaseModel import init
from app.routers.v1.ClientRouter import ClientRouter
from app.routers.v1.UserRouter import UserRouter

# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(title=env.APP_NAME, version=env.API_VERSION, openapi_tags=Tags)

# Add Routers
app.include_router(ClientRouter)
app.include_router(UserRouter)

# Initialise Data Model Attributes
init()
