from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import filters
from config import API_HASH, API_ID, PHONE
from pyrogram.enums import ParseMode
import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../bot.log"),  # Log to a file
        logging.StreamHandler(),  # Log to console
    ],
)

logger = logging.getLogger(__name__)

# Define your API ID, Hash, and the phone number associated with your Telegram account
api_id = API_ID
api_hash = API_HASH
phone = PHONE

# Define source and destination channels
# source_channel_a = "https://t.me/signalsbitcoinandethereum"
# source_channel_b = "https://t.me/+-ATPIPjdgP43OWUy"
# main_channel = 'https://t.me/alex_cryptomaster'
# premium_channel = "https://t.me/premium_channel"


# source_channel_a = -1001792317500 #test
source_channel_a = -1001746203369
status_determine_handler_one = False
is_media_group_handler_one = False

source_channel_b = -1002243037651  # test
source_channel_b1 = -1002174970069  # test
source_channel_b2 = -1001206076820  # test
# source_channel_b = -1001742512586
status_determine_handler_two = False
is_media_group_handler_two = False


source_channel_premium = -1001979487373
status_determine_handler_premium = False
is_media_group_handler_premium = False


main_channel = int(-1002106528369)
premium_channel = int(-1002235324140)

# Create a Telegram client
# client = Client(name="messageForwardBotTest", api_id=api_id, api_hash=api_hash)
client = Client(name="messageForwardBot", api_id=api_id, api_hash=api_hash)


# Helper function to replace text
def replace_text(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def check_link(text):
    if not text:
        return

    if "https://www.bybit.com/" in text or "https" in text:
        return True

    # if "https://www.bybit.com/" in text:
    #     return True

    return False


def check_champ(text):
    if not text:
        return

    if "European Football Championship" in text:
        return True

    return False


@client.on_message(filters=filters.chat(source_channel_a) & filters.sticker)
async def handler_group_one_sticker(client: Client, message: Message):
    await client.copy_message(main_channel, source_channel_a, message.id)


@client.on_message(filters=(filters.chat(source_channel_b)) & filters.sticker)
async def handler_group_two_sticker(client: Client, message: Message):
    await client.copy_message(main_channel, source_channel_b, message.id)


@client.on_message(filters=filters.chat(source_channel_premium) & filters.sticker)
async def handler_group_premium_sticker(client: Client, message: Message):
    await client.copy_message(premium_channel, source_channel_premium, message.id)


@client.on_message(filters=filters.chat(source_channel_a))
async def handler_group_one(client: Client, message: Message):
    global is_media_group_handler_one, status_determine_handler_one

    logging.info("handler_group_one ")
    logging.info("Message Text: " + (message.text if message.text else "None"))
    logging.info(
        "message.media_group_id: "
        + (message.media_group_id if message.media_group_id else "None")
    )
    logging.info(
        "message.video and message.caption: "
        + (
            (message.video and message.caption)
            if message.video and message.caption
            else "None"
        )
    )
    logging.info(
        "message.photo and message.caption: "
        + (
            (message.photo and message.caption)
            if message.photo and message.caption
            else "None"
        )
    )

    if (
        check_link(message.text)
        or check_link(message.caption)
        or check_champ(message.text)
        or check_champ(message.caption)
    ):
        logging.info("Wrong Message")
        return

    if not status_determine_handler_one:
        if message.media_group_id:
            if is_media_group_handler_one:
                return

            logger.info("Send MediaGroup")
            replacements = {"@SignalsOw": "@crytpmasteralex"}

            is_media_group_handler_one = True
            status_determine_handler_one = True

            new_message = await client.copy_media_group(
                main_channel, source_channel_a, message.id
            )

            await asyncio.sleep(2)

            is_media_group_handler_one = False
            status_determine_handler_one = False

            try:
                await client.edit_message_caption(
                    main_channel,
                    new_message[0].id,
                    replace_text(new_message[0].caption, replacements),
                )
            except Exception as ex:
                logging.info(ex)

        elif message.video:
            replacements = {"@SignalsOw": "@crytpmasteralex"}
            video = message.video.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_video(
                main_channel,
                video=video,
                caption=caption,
            )
        elif message.photo:
            replacements = {"@SignalsOw": "@crytpmasteralex"}
            photo = message.photo.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_photo(
                main_channel,
                photo=photo,
                caption=caption,
            )

        elif message.text:
            replacements = {"@SignalsOw": "@crytpmasteralex"}

            new_txt = replace_text(message.text, replacements)
            await client.send_message(
                main_channel,
                new_txt,
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        if is_media_group_handler_one:
            return


@client.on_message(
    filters=(
        filters.chat(source_channel_b)
        | filters.chat(source_channel_b1)
        | filters.chat(source_channel_b2)
    )
)
async def handler_group_two(client: Client, message: Message):
    global is_media_group_handler_two, status_determine_handler_two

    logging.info(f"handler_group_two {message.chat.id} ")
    logging.info("Message Text: " + (message.text if message.text else "None"))
    logging.info(
        "message.media_group_id: "
        + (str(message.media_group_id) if message.media_group_id else "None")
    )
    logging.info(
        "message.video and message.caption: "
        + (
            (message.video and message.caption)
            if message.video and message.caption
            else "None"
        )
    )
    logging.info(
        "message.photo and message.caption: "
        + (
            (message.photo and message.caption)
            if message.photo and message.caption
            else "None"
        )
    )

    if (
        check_link(message.text)
        or check_link(message.caption)
        or check_champ(message.text)
        or check_champ(message.caption)
    ):
        logging.info("Wrong Message")
        return

    if not status_determine_handler_two:
        if message.media_group_id:
            if is_media_group_handler_two:
                return

            logger.info("Send MediaGroup")
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}

            is_media_group_handler_two = True
            status_determine_handler_two = True

            new_message = await client.copy_media_group(
                main_channel, source_channel_b, message.id
            )

            await asyncio.sleep(2)

            is_media_group_handler_two = False
            status_determine_handler_two = False

            try:
                await client.edit_message_caption(
                    main_channel,
                    new_message[0].id,
                    replace_text(new_message[0].caption, replacements),
                )
            except Exception as ex:
                logging.info(ex)

        elif message.video:
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}
            video = message.video.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_video(
                main_channel,
                video=video,
                caption=caption,
            )
        elif message.photo:
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}
            photo = message.photo.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_photo(
                main_channel,
                photo=photo,
                caption=caption,
            )

        elif message.text:
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}

            new_txt = replace_text(message.text, replacements)
            await client.send_message(
                main_channel,
                new_txt,
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        if is_media_group_handler_two:
            return


@client.on_message(filters=filters.chat(source_channel_premium))
async def handler_group_premium(client: Client, message: Message):
    global is_media_group_handler_two, status_determine_handler_two

    logging.info("handler_group_premium ")
    logging.info("Message Text: " + (message.text if message.text else "None"))
    logging.info(
        "message.media_group_id: "
        + (message.media_group_id if message.media_group_id else "None")
    )
    logging.info(
        "message.video and message.caption: "
        + (
            (message.video and message.caption)
            if message.video and message.caption
            else "None"
        )
    )
    logging.info(
        "message.photo and message.caption: "
        + (
            (message.photo and message.caption)
            if message.photo and message.caption
            else "None"
        )
    )

    if (
        check_link(message.text)
        or check_link(message.caption)
        or check_champ(message.text)
        or check_champ(message.caption)
    ):
        logging.info("Wrong Message")
        return

    if not status_determine_handler_two:
        if message.media_group_id:
            if is_media_group_handler_two:
                return

            logger.info("Send MediaGroup")
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}

            is_media_group_handler_two = True
            status_determine_handler_two = True

            new_message = await client.copy_media_group(
                premium_channel, source_channel_premium, message.id
            )

            await asyncio.sleep(2)

            is_media_group_handler_two = False
            status_determine_handler_two = False

            try:
                await client.edit_message_caption(
                    premium_channel,
                    new_message[0].id,
                    replace_text(new_message[0].caption, replacements),
                )
            except Exception as ex:
                logging.info(ex)

        elif message.video:
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}
            video = message.video.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_video(
                premium_channel,
                video=video,
                caption=caption,
            )
        elif message.photo:
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}
            photo = message.photo.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_photo(
                premium_channel,
                photo=photo,
                caption=caption,
            )

        elif message.text:
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}

            new_txt = replace_text(message.text, replacements)
            await client.send_message(
                premium_channel,
                new_txt,
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        if is_media_group_handler_two:
            return


def zaglushka(client: Client, message: Message):
    logging.info("zagkushka")


client.add_handler(
    MessageHandler(
        zaglushka,
        (
            filters.chat(source_channel_a)
            | filters.chat(source_channel_b)
            | filters.chat(source_channel_premium)
        )
        & filters.poll,
    )
)

client.run()
