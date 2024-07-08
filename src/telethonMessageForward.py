from telethon import TelegramClient, events
from telethon.types import (
    Message,
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaPoll,
    MessageMediaEmpty,
)
from config import API_HASH, API_ID, PHONE

import asyncio
import logging
import os
import pprint

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


main_channel = int(-1002227848813)

# Create a Telegram client

client = TelegramClient("telethonMessageForwardBot", api_id=api_id, api_hash=api_hash)

mediaGroup_1 = []
mediaGroup_2 = []


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


entity_ids = [
    -1001746203369,
    -1001742512586,
    -1002191626337,
    -1001871051921,
    -1001876753838,
    -1002121017957,
    -1002169930605,
]


is_media_group = False


async def forward_anonim_message(event, text):
    replacements_source_1 = {"@SignalsOw": "@crytpmasteralex"}
    replacements_source_2 = {"@bybitpro_michael": "@crytpmasteralex"}

    text = replace_text(text, replacements_source_1)
    text = replace_text(text, replacements_source_2)

    if isinstance(event.message.media, MessageMediaPhoto):
        logging.info("Photo: " + str(event.message.media.photo))
        photo_folder = f"./{event.message.media.photo.id}"
        photo_file = await client.download_media(
            event.message.media, f"{photo_folder}/photo"
        )
        await client.send_file(main_channel, photo_file, caption=text)
        logging.info(photo_folder)
        logging.info(photo_file)
        os.remove(photo_file)
        os.rmdir(photo_folder)
    elif isinstance(event.message.media, MessageMediaDocument):
        logging.info("Document: " + str(event.message.media.document))
        await client.send_file(main_channel, event.message.media.document, caption=text)
    elif isinstance(event.message.media, MessageMediaPoll):
        return
    else:
        await client.send_message(main_channel, text)


async def _get_media_posts_in_group(chat, original_post, max_amp=10):
    """
    Searches for Telegram posts that are part of the same group of uploads
    The search is conducted around the id of the original post with an amplitude
    of `max_amp` both ways
    Returns a list of [post] where each post has media and is in the same grouped_id
    """
    if original_post.grouped_id is None:
        return [original_post] if original_post.media is not None else []

    search_ids = [
        i for i in range(original_post.id - max_amp, original_post.id + max_amp + 1)
    ]
    posts = await client.get_messages(chat, ids=search_ids)
    media = []
    for post in posts:
        if (
            post is not None
            and post.grouped_id == original_post.grouped_id
            and post.media is not None
        ):
            media.append(post)
    return media


@client.on(events.NewMessage(entity_ids))
async def newMessage(event):
    global is_media_group, mediaGroup_1
    chat = await event.get_chat()
    chat_id = event.chat_id
    text = event.message.message
    # logging.info(event)

    if check_champ(text) or check_link(text):
        return

    if event.message.grouped_id:

        if not is_media_group:
            is_media_group = True
            id = event.message.grouped_id
            messages = await _get_media_posts_in_group(chat, event.message)
            text = ""
            c = 0
            for i in messages:
                if c == 0:
                    text = i.message
                    c += 1

                photo_file = await client.download_media(i.media, f"{id}/file")
                mediaGroup_1.append(photo_file)

            await client.send_file(main_channel, mediaGroup_1, caption=text)

            mediaGroup_1 = []
            c = 0

            for i in mediaGroup_1:
                os.remove(i)

            os.rmdir(str(id))
            await asyncio.sleep(5)
            is_media_group = False

    else:
        await forward_anonim_message(event, text)


client.start(phone)
with client:
    client.run_until_disconnected()
