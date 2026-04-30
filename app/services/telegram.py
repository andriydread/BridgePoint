import logging
from datetime import datetime
from typing import Optional, Tuple
from zoneinfo import ZoneInfo

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_localized_time() -> str:
    """Returns the current time formatted as a string based on APP_TIMEZONE."""
    try:
        tz = ZoneInfo(settings.APP_TIMEZONE)
    except Exception:
        tz = ZoneInfo("UTC")

    local_now = datetime.now(tz)
    return local_now.strftime("%d %b, %H:%M")


async def send_telegram_message(message: str) -> Tuple[bool, Optional[int]]:
    """
    Sends a new message to the configured Telegram chat
    Returns (success, message_id)
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

    timestamp = get_localized_time()
    formatted_message = f"<b>Last Update: {timestamp}</b>\n\n{message}"

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": formatted_message,
        "parse_mode": "HTML",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            message_id = data.get("result", {}).get("message_id")
            return True, message_id
        except httpx.HTTPStatusError as e:
            logger.error(f"Telegram API error: {e.response.text}")
            return False, None
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False, None


async def edit_telegram_message(message_id: int, new_text: str) -> bool:
    """
    Updates an existing message in the Telegram chat
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/editMessageText"

    timestamp = get_localized_time()
    formatted_message = f"<b>Last Update: {timestamp}</b>\n\n{new_text}"

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "message_id": message_id,
        "text": formatted_message,
        "parse_mode": "HTML",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            logger.error(f"Telegram API error while editing: {e.response.text}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error editing Telegram message: {e}")
            return False
