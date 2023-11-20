from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase
from urllib.parse import quote_plus
from fastapi import FastAPI

username = 'chapadiyahansil'
password = 'hansil@714'

# Escape username and password using quote_plus()
escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

client = AsyncIOMotorClient(f'mongodb+srv://{escaped_username}:{escaped_password}@cluster0.grvhoxa.mongodb.net/?authMechanism=DEFAULT')
database = client['SSIP-Hackathon']

async def connect_to_mongo(app: FastAPI):
    app.state.mongodb = database  # Attach the database connection to the app state
    app.state.mongodb_client = client  # Attach the client for closing later
    # app.database = database  # Attach the database connection to the app object


# Function to get the database
async def get_database() -> AsyncIOMotorDatabase:
    return database
    # # ... rest of your database connection logic
