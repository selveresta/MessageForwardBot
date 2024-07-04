from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import filters
from config import API_HASH, API_ID, PHONE
from pyrogram.enums import ParseMode
import asyncio

# Define your API ID, Hash, and the phone number associated with your Telegram account
api_id = API_ID
api_hash = API_HASH
phone = PHONE

# Define source and destination channels
# source_channel_a = "https://t.me/signalsbitcoinandethereum"
# source_channel_b = "https://t.me/+-ATPIPjdgP43OWUy"
# main_channel = 'https://t.me/alex_cryptomaster'
# premium_channel = "https://t.me/premium_channel"


source_channel_a = -1001746203369
source_channel_a_link = "https://t.me/signalsbitcoinandethereum"
status_determine_handler_one = False
is_media_group_handler_one = False
is_photo_handler_one = False
is_text_handler_one = False

source_channel_b = -1001742512586
source_channel_b_link = "https://t.me/+-ATPIPjdgP43OWUy"

status_determine_handler_two = False
is_media_group_handler_two = False
is_photo_handler_two = False
is_text_handler_two = False


source_channel_premium = -1001979487373
# source_channel_premium_link = -1001746203369
status_determine_handler_premium = False
is_media_group_handler_premium = False
is_photo_handler_premium = False
is_text_handler_premium = False


main_channel = int(-1002106528369)
main_channel_link = int(-1002106528369)
premium_channel = int(-1002235324140)

# Create a Telegram client
client = Client(name="messageForwardBot", api_id=api_id, api_hash=api_hash)


# Helper function to replace text
def replace_text(text, replacements):
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def check_link(text):
    if "https://www.bybit.com/" in text:
        return True

    return False


def check_champ(text):
    if "European Football Championship" in text:
        return True

    return False


async def handler_group_one(client: Client, message: Message):
    global is_media_group_handler_one, is_photo_handler_one, is_text_handler_one, status_determine_handler_one
    print("handler_group_one ")
    print("Message Text: ", message.text)
    print("message.media_group_id: ", message.media_group_id)
    print("message.video and message.caption: ", (message.video and message.caption))
    print("message.photo and message.caption: ", (message.photo and message.caption))
    # if (
    #     check_link(message.text)
    #     or check_link(message.caption)
    #     or check_champ(message.text)
    #     or check_champ(message.caption)
    # ):
    #     return

    if not status_determine_handler_one:
        if message.media_group_id:
            if is_media_group_handler_one:
                return
            replacements = {"@SignalsOw": "@crytpmasteralex"}

            is_media_group_handler_one = True
            status_determine_handler_one = True

            new_message = await client.copy_media_group(
                main_channel_link, source_channel_a, message.id
            )

            await asyncio.sleep(2)

            is_media_group_handler_one = False
            status_determine_handler_one = False

            try:
                await client.edit_message_caption(
                    main_channel_link,
                    new_message[0].id,
                    replace_text(new_message[0].caption, replacements),
                )
            except Exception as ex:
                print(ex)

        elif message.video and message.caption:
            replacements = {"@SignalsOw": "@crytpmasteralex"}
            video = message.video.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_video(
                main_channel_link,
                video=video,
                caption=caption,
            )
        elif message.photo and message.caption:
            replacements = {"@SignalsOw": "@crytpmasteralex"}
            photo = message.photo.file_id
            caption = (
                replace_text(message.caption, replacements) if message.caption else ""
            )
            await client.send_photo(
                main_channel_link,
                photo=photo,
                caption=caption,
            )

        else:
            replacements = {"@SignalsOw": "@crytpmasteralex"}

            new_txt = replace_text(message.text, replacements)
            await client.send_message(
                main_channel_link,
                new_txt,
                parse_mode=ParseMode.MARKDOWN,
            )
    else:
        if is_media_group_handler_one:
            return


async def handler_group_two(client: Client, message: Message):
    global is_media_group_handler_two, is_photo_handler_two, is_text_handler_two, status_determine_handler_two

    print("handler_group_two ")
    print("Message Text: ", message.text)
    print("message.media_group_id: ", message.media_group_id)
    print("message.video and message.caption: ", (message.video and message.caption))
    print("message.photo and message.caption: ", (message.photo and message.caption))

    if (
        check_link(message.text)
        or check_link(message.caption)
        or check_champ(message.text)
        or check_champ(message.caption)
    ):
        return

    if not status_determine_handler_two:
        if message.media_group_id:
            if is_media_group_handler_two:
                return
            replacements = {"@bybitpro_michael": "@crytpmasteralex"}

            is_media_group_handler_two = True
            status_determine_handler_two = True

            new_message = await client.copy_media_group(
                main_channel, source_channel_a, message.id
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
                print(ex)

        elif message.video or message.caption:
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
        elif message.photo or message.caption:
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

        else:
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


async def handler_group_premium(client: Client, message: Message):
    global is_media_group_handler_two, is_photo_handler_two, is_text_handler_two, status_determine_handler_two

    print("handler_group_premium ")
    print("Message Text: ", message.text)
    print("message.media_group_id: ", message.media_group_id)
    print("message.video and message.caption: ", (message.video and message.caption))
    print("message.photo and message.caption: ", (message.photo and message.caption))

    if (
        check_link(message.text)
        or check_link(message.caption)
        or check_champ(message.text)
        or check_champ(message.caption)
    ):
        return

    if not status_determine_handler_two:
        if message.media_group_id:
            if is_media_group_handler_two:
                return
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
                print(ex)

        elif message.video or message.caption:
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
        elif message.photo or message.caption:
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

        else:
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


async def handler_group_one_sticker(client: Client, message: Message):
    await client.copy_message(main_channel, source_channel_a, message.id)


async def handler_group_two_sticker(client: Client, message: Message):
    await client.copy_message(main_channel, source_channel_b, message.id)


def zaglushka(client: Client, message: Message):
    print("zagkushka")
    pass


client.add_handler(
    MessageHandler(
        zaglushka,
        filters.chat(source_channel_a) & filters.poll,
    )
)

client.add_handler(
    MessageHandler(
        handler_group_one_sticker,
        filters=filters.sticker & filters.chat(source_channel_a),
    )
)

client.add_handler(
    MessageHandler(
        handler_group_two_sticker,
        filters=filters.sticker & filters.chat(source_channel_b),
    )
)


client.add_handler(
    MessageHandler(handler_group_one, filters=filters.chat(source_channel_a))
)

client.add_handler(
    MessageHandler(handler_group_two, filters=filters.chat(source_channel_b))
)


client.add_handler(
    MessageHandler(handler_group_premium, filters=filters.chat(source_channel_premium))
)


client.run()
