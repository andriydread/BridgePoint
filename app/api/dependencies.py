from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.db.models import Application
from app.core.security import hash_api_key

async def verify_api_key(
    x_api_key: str = Header(..., description="API Key for the application"),
    db: AsyncSession = Depends(get_db)
) -> Application:
    hashed_key = hash_api_key(x_api_key)
    
    query = select(Application).where(Application.api_key_hash == hashed_key)
    result = await db.execute(query)
    application = result.scalar_one_or_none()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return application
