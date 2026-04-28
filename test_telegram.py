import asyncio
from app.services.telegram import send_telegram_message
from dotenv import load_dotenv

async def main():
    print("Test start")
    success = await send_telegram_message("This is a test message")
    if success:
        print("Message sent successfully")
    else:
        print("Failed to send message")

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
