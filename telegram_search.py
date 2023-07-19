from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

from telethon import TelegramClient
from telethon.tl.types import Channel, Megagroup
from tqdm import tqdm
import csv
import asyncio

# Use your own api_id and api_hash
api_id = "ICCHelperBot"
api_hash = '6049845722:AAF3Lqf_kBqNJll_7PK_sVGBTwr5Gpa2Kfs'


async def run():
    # Connect to Telegram using Telethon
    async with TelegramClient('session_name', api_id, api_hash) as client:
        await client.start()

        # Open the keywords file
        with open('keywords.txt', 'r') as f:
            keywords = f.readlines()

        # Remove the newline characters from the keywords
        keywords = [k.strip() for k in keywords]

        # Open a CSV file to write the search results
        with open('search_results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Username', 'Message', 'Date', 'Link', 'Keyword'])

            # Get all the chats
            chats = await client.get_dialogs()

            # Find the desired channel by username or title
            desired_channel = None
            for chat in chats:
                if isinstance(chat.entity, Channel) or isinstance(chat.entity, Megagroup):
                    if chat.entity.username == 'your_channel_username':
                        desired_channel = chat
                        break

            # Use a progress bar to show the progress
            for chat in tqdm(chats):
                try:
                    if isinstance(chat.entity, Channel) or isinstance(chat.entity, Megagroup):
                        # Get all the messages in the chat
                        messages = await client.get_messages(chat, limit=100), filter = Filters.photo

                        # Iterate through the messages
                        for message in messages:
                            # Check if any of the keywords are in the message text
                            for keyword in keywords:
                                if keyword in message.message:
                                    # Write the username, message text, date, link and keyword to the CSV file
                                    writer.writerow([message.from_id, message.message, message.date,
                                                     f'https://t.me/{chat.entity.username}', keyword])

                # Use a progress bar to show the progress
                for message in tqdm(await client.get_messages(desired_channel, limit=100)):
                    # Check if any of the keywords are in the message text
                    for keyword in keywords:
                        if keyword in message.message:
                            # Write the username, message text, date, link, and keyword to the CSV file
                            writer.writerow([message.from_id, message.message, message.date,
                                             f'https://t.me/{desired_channel.entity.username}', keyword])
                            # Check if the message contains a photo
                            # if message.photo:
                            #     # Process the photo here, you can access different sizes and other photo details
                            #     # using the 'message.photo' attribute
                            #     # For example, you can access the largest photo size with:
                            #     largest_photo = message.photo[-1]
                            #     # Do whatever you want with the photo, such as downloading or processing it
                            #     # You can also write the relevant details to the CSV file if needed
                            #     # Check if the message contains a photo
                            if message.photo:
                                # Process the photo here
                                for photo in message.photo:
                                    # Download the photo
                                    photo_path = await client.download_media(photo)

                                    # Open the photo using PIL
                                    with Image.open(photo_path) as img:
                                        # Extract the Exif data
                                        exif_data = img._getexif()

                                        # Do whatever you want with the Exif data
                                        # You can save it to the CSV file or perform any other desired operations

                except Exception as e:
                # Handle any exceptions that occur
                print(f"Error: {e}")


asyncio.run(run())
