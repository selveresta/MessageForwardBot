from telethon import TelegramClient, events
from telethon.types import (
    MessageMediaPhoto,
    MessageMediaDocument,
    MessageMediaPoll,
)
from config import API_HASH, API_ID, PHONE
from telethon import utils

import asyncio
import logging
import os

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


main_channel = int(-1002247420892)
# premium_channel = int(-1002227848813)

# Create a Telegram client

# client = TelegramClient("telethonMessageForwardBot", api_id=api_id, api_hash=api_hash)

with TelegramClient("telethonMessageForwardBot", api_id, api_hash) as client:
    # Helper function to replace text
    mediaGroup_1 = []
    is_media_group = False

    source_one_two = [-1001742512586, -1002227848813]
    source_two = [-1001746203369]

    source_premium = [
        -1001746203369,
    ]

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

        if (
            "European Football Championship" in text
            or "match" in text
            or "semi-final" in text
        ):
            return True

        return False

    async def forward_anonim_message(event, text, channel):
        replacements_source = {
            "@SignalsOw": "@crytpmasteralex",
            "@bybitpro_michael": "@crytpmasteralex",
        }

        text = replace_text(text, replacements_source)
        try:
            if isinstance(event.message.media, MessageMediaPhoto):
                logging.info("Photo: " + str(event.message.media.photo))
                photo_folder = f"./{event.message.media.photo.id}"
                photo_file = await client.download_media(
                    event.message.media, f"{photo_folder}/photo"
                )
                await client.send_file(channel, photo_file, caption=text)
                logging.info(photo_folder)
                logging.info(photo_file)
                os.remove(photo_file)
                os.rmdir(photo_folder)
            elif isinstance(event.message.media, MessageMediaDocument):
                logging.info("Document: " + str(event.message.media.document))
                await client.send_file(
                    channel, event.message.media.document, caption=text
                )
            elif isinstance(event.message.media, MessageMediaPoll):
                return
            else:
                await client.send_message(channel, text)
        except Exception as ex:
            logging.error(ex)
            os.remove(photo_file)
            os.rmdir(photo_folder)

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

    @client.on(events.NewMessage(from_users=[6229293964]))
    async def newMessage(event):
        global is_media_group, mediaGroup_1, source_two
        for i in source_two:
            real_id, peer_type = utils.resolve_id(i)

            chat = await event.get_chat()
            if chat.id == real_id:
                text = event.message.message

                if check_champ(text) or check_link(text):
                    return

                if event.message.grouped_id:
                    replacements_source = {
                        "@SignalsOw": "@crytpmasteralex",
                        "@bybitpro_michael": "@crytpmasteralex",
                    }

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

                            photo_file = await client.download_media(
                                i.media, f"{id}/file"
                            )
                            mediaGroup_1.append(photo_file)

                        text = replace_text(text, replacements_source)
                        try:
                            await client.send_file(
                                main_channel, mediaGroup_1, caption=text
                            )

                            for i in mediaGroup_1:
                                os.remove(i)

                            mediaGroup_1 = []
                            c = 0

                            os.rmdir(str(id))
                            await asyncio.sleep(5)
                            is_media_group = False
                        except:
                            for i in mediaGroup_1:
                                os.remove(i)

                            mediaGroup_1 = []
                            c = 0

                            os.rmdir(str(id))
                            await asyncio.sleep(5)
                            is_media_group = False

                else:
                    await forward_anonim_message(event, text, main_channel)

    @client.on(events.NewMessage)
    async def newMessage(event):
        global is_media_group, mediaGroup_1, source_one_two
        for i in source_one_two:
            real_id, peer_type = utils.resolve_id(i)

            chat = await event.get_chat()
            if chat.id == real_id:
                text = event.message.message

                if check_champ(text) or check_link(text):
                    return

                if event.message.grouped_id:
                    replacements_source = {
                        "@SignalsOw": "@crytpmasteralex",
                        "@bybitpro_michael": "@crytpmasteralex",
                    }

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

                            photo_file = await client.download_media(
                                i.media, f"{id}/file"
                            )
                            mediaGroup_1.append(photo_file)

                        text = replace_text(text, replacements_source)

                        await client.send_file(main_channel, mediaGroup_1, caption=text)

                        for i in mediaGroup_1:
                            os.remove(i)

                        mediaGroup_1 = []
                        c = 0

                        os.rmdir(str(id))
                        await asyncio.sleep(5)
                        is_media_group = False

                else:
                    await forward_anonim_message(event, text, main_channel)

    client.start()
    client.run_until_disconnected()


# @client.on(events.NewMessage(source_premium))
# async def newMessagePremium(event):
#     global is_media_group, mediaGroup_1
#     chat = await event.get_chat()
#     text = event.message.message
#     logging.info(event)

#     if check_champ(text) or check_link(text):
#         return

#     if event.message.grouped_id:
#         if not is_media_group:
#             is_media_group = True
#             id = event.message.grouped_id
#             messages = await _get_media_posts_in_group(chat, event.message)
#             text = ""
#             c = 0
#             for i in messages:
#                 if c == 0:
#                     text = i.message
#                     c += 1

#                 photo_file = await client.download_media(i.media, f"{id}/file")
#                 mediaGroup_1.append(photo_file)

#             await client.send_file(main_channel, mediaGroup_1, caption=text)

#             for i in mediaGroup_1:
#                 os.remove(i)

#             mediaGroup_1 = []
#             c = 0

#             os.rmdir(str(id))
#             await asyncio.sleep(5)
#             is_media_group = False

#     else:
#         await forward_anonim_message(event, text, premium_channel)
