import logging
import os
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from dotenv import load_dotenv
import json
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
import pandas as pd

from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

load_dotenv()

API_TOKEN = str(os.environ.get("BOT_API_TOKEN", 0))

main_channel = int(-1002247420892)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("./welcome.log"),  # Log to a file
        logging.StreamHandler(),  # Log to console
    ],
)

logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()


def save_user(message: CallbackQuery):
    with open("users.json", "r") as file:
        db = json.load(file)

        users = db.get("users")

        for i in users:
            if int(i["id"]) == message.from_user.id:
                return

        user = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "name": message.from_user.first_name,
            "sub": False,
        }

        users.append(user)
        db["users"] = users

        with open("users.json", "w") as out_file:
            json.dump(db, out_file)


def update_user(id):
    with open("users.json", "r") as file:
        db = json.load(file)

        users = db.get("users")

        for i in users:
            if int(i["id"]) == id:
                i["sub"] = True
                db["users"] = users

                with open("users.json", "w") as out_file:
                    json.dump(db, out_file)

                break


def get_users():
    with open("users.json", "r") as file:
        db = json.load(file)
        users = db.get("users")

        return users


class testCl(CallbackData, prefix="notifFinal"):
    test: str


@router.message(Command("start"))
async def send_welcome(message: Message):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text="CONFIRM",
            callback_data=testCl(test="test").pack(),
        )
    )

    k = keyboard.as_markup()

    await message.answer(text="Confirm you are not a bot 🤖", reply_markup=k)


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_member(event: ChatMemberUpdated, bot: Bot):
    update_user(event.from_user.id)


@router.callback_query(testCl.filter())
async def send_welcome(message: CallbackQuery):
    save_user(message)
    await bot.send_message(
        message.from_user.id,
        "Welcome subscribe to this Channel\n⬇️⬇️⬇️⬇️\n\nhttps://t.me/alex_cryptomaster",
    )
    await message.answer()


@router.message(Command("pinnedMessage"))
async def send_welcome(message: Message):
    img = FSInputFile("img2.jpg")

    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text="CHAT WITH ADMIN",
            url="https://t.me/crytpmasteralex",
        )
    )

    k = keyboard.as_markup()

    text = """
🔥 All Or Nothing Day 🔥

Guys, what I’ve got to do with you 🧐

I think you didn’t quite get the thing, the sense of yesterday’s promotion 🙂

The thing was that you ought to choose ALL each day, not only once 😎

Choosing ALL instead of mediocrity is the path, the lifestyle of a real trader 💪

I wanted to motivate you for changes using this philosophy. Well, those 15 guys who joined us the day before are now already cutting cash from our calls 🔥

So, closer to the deal. I decided to make an exception today and extend the promotion on the same conditions 💯

Though there will be 🔟 places only this time 😈

Grab your hands in legs and choose ALL with us! Nothing will be left for losers 🖤

💸 VIP-Membership Price: 💸

$999 — $499 (lifetime)

Write to me right now Or use our bot for payment 👇
"""

    await bot.send_photo(chat_id=main_channel, caption=text, photo=img, reply_markup=k)


@router.message(Command("statistic"))
async def send_welcome(message: Message):
    users = get_users()

    flattened_data = []
    for user in users:

        flattened_entry = {
            "id": user["id"],
            "username": user["username"],
            "name": user["name"],
            "sub": user["sub"],
        }
        flattened_data.append(flattened_entry)

    # Create a DataFrame and save to Excel
    df = pd.DataFrame(flattened_data)

    with pd.ExcelWriter("subs.xlsx", engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Subscribers", index=False)

    file = FSInputFile("subs.xlsx")
    await bot.send_document(message.from_user.id, file)


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
