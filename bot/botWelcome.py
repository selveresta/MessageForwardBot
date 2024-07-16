import logging
import os
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = str(os.environ.get("BOT_API_TOKEN", 0))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()


@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Welcome subscribe to this Channel\n⬇️⬇️⬇️⬇️\n\nhttps://t.me/alex_cryptomaster"
    )


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
