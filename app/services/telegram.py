import logging
from typing import Optional, Tuple

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_telegram_message(message: str) -> Tuple[bool, Optional[int]]:
    """
    Sends a new message to the configured Telegram chat
    Returns (success, message_id)
    """
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message,
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
    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "message_id": message_id,
        "text": new_text,
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
