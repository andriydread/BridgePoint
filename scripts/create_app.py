import asyncio
import secrets
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.db.database import SessionLocal
from app.db.models import Application
from app.core.security import hash_api_key

async def create_app(name: str):
    async with SessionLocal() as session:
        raw_api_key = secrets.token_urlsafe(32)
        hashed_key = hash_api_key(raw_api_key)
        
        new_app = Application(name=name, api_key=hashed_key)
        session.add(new_app)
        await session.commit()
        
        print(f"Created application: {name}")
        print(f"API Key: {raw_api_key}")
        print("IMPORTANT: Save this key! It will be hashed in the database and cannot be recovered")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/create_app.py <app_name>")
    else:
        asyncio.run(create_app(sys.argv[1]))
