from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import verify_api_key
from app.db.database import get_db
from app.db.models import Application, NotificationLog
from app.schemas.payload import NotificationPayload
from app.services.telegram import send_telegram_message

router = APIRouter(prefix="/notify", tags=["Notifications"])

@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def notify(
    payload: NotificationPayload,
    application: Application = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db)
):
    # Send Telegram message
    success = await send_telegram_message(payload.message)
    
    # Log the notification
    log = NotificationLog(
        application_id=application.id,
        message=payload.message,
        status="sent" if success else "failed"
    )
    db.add(log)
    await db.commit()
    
    return {"status": "success" if success else "failed"}
