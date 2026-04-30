from fastapi import APIRouter, Depends, status
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import verify_api_key
from app.db.database import get_db
from app.db.models import Application, NotificationLog
from app.schemas.payload import NotificationPayload
from app.services.telegram import edit_telegram_message, send_telegram_message

router = APIRouter(prefix="/notify", tags=["Notifications"])


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def notify(
    payload: NotificationPayload,
    application: Application = Depends(verify_api_key),
    db: AsyncSession = Depends(get_db),
):
    # Look for the last successful message from this application
    query = (
        select(NotificationLog)
        .where(NotificationLog.application_id == application.id)
        .where(NotificationLog.telegram_message_id.is_not(None))
        .order_by(desc(NotificationLog.created_at))
        .limit(1)
    )
    result = await db.execute(query)
    last_log = result.scalar_one_or_none()

    success = False
    msg_id = None

    # Try to edit if a previous message exists
    if last_log:
        success = await edit_telegram_message(
            last_log.telegram_message_id, payload.message
        )
        if success:
            msg_id = last_log.telegram_message_id

    # If no previous message or edit failed, send new one
    if not success:
        success, msg_id = await send_telegram_message(payload.message)

    # Log the transaction
    log = NotificationLog(
        application_id=application.id,
        message=payload.message,
        status="sent" if success else "failed",
        telegram_message_id=msg_id,
    )
    db.add(log)
    await db.commit()

    return {"status": "success" if success else "failed"}
