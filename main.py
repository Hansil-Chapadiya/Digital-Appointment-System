# main.py
from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import OAuthFlowAuthorizationCode as OAuthFlowAuthorizationCodeModel
from fastapi.security import OAuth2AuthorizationCodeBearer
from router import AdminRouter
from Controller.db_init import connect_to_mongo

app = FastAPI()

async def lifespan(app: FastAPI):
    await connect_to_mongo(app)

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="token",tokenUrl="token")

app.include_router(AdminRouter)