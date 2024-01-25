# Author: Fayas (https://github.com/FayasNoushad)

import os
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pypi import pypi_text, pypi_buttons


load_dotenv()

START_TEXT = """
Hello {},
I am a pypi package search telegram bot.

- Send a pypi package name.
- I will send the information of package.
"""

BUTTONS = [InlineKeyboardButton('⚙ Feedback ⚙', url='https://telegram.me/FayasNoushad')]

Bot = Client(
    "PyPi-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command(["start", "help", "about"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = InlineKeyboardMarkup([BUTTONS])
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@Bot.on_message(filters.text)
async def pypi_info(bot, update):
    
    message = await update.reply_text(
        text="Checking...",
        quote=True
    )
    
    try:
        
        chat_type = update.chat.type
        text = update.text
    
        # Check chat type private or not
        if (chat_type==ChatType.PRIVATE):
            query = text
        else:
            query = text.split()[1]
        
        # get text and buttons from pypi.py file
        text = pypi_text(query)
        buttons = pypi_buttons(query)
        
        # reply package informations
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=buttons
        )
        
    except Exception as e:
        # print(e)
        await message.edit_text(
            text="Something went wrong"
        )


Bot.run()
