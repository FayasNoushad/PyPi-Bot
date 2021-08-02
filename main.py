# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


API = "https://api.abirhasan.wtf/pypi?query="

START_TEXT = """
Hello {},
I am a pypi package search telegram bot.

- Send a pypi package name.
- I will send the information of package.

Made by @FayasNoushad
"""

BUTTONS = [InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')]

Bot = Client(
    "PyPi-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = InlineKeyboardMarkup(BUTTONS)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


@Bot.on_message(filters.text)
async def pypi_info(bot, update):
    query = update.text if update.chat.type == "private" else update.text.split()[1]
    text = pypi_text(query)
    reply_markup = InlineKeyboardMarkup(pypi_buttons(query), BUTTONS)
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )


def pypi(query):
    r = requests.get(API + query)
    info = r.json()
    return info


def pypi_text(query):
    info = pypi(query)
    text = "--**Information**--\n"
    text += f"\n**Package Name:** `{info['PackageName']}`"
    text += f"\n**Title:** `{info['Title']}`"
    text += f"\n**About:** `{info['About']}`"
    text += f"\n**Latest Release Date:**`{info['LatestReleaseDate']}`"
    text += f"\n**PiP Command:** `{info['PipCommand']}`"
    return text


def pypi_buttons(query):
    info = pypi(query)
    buttons = [
        InlineKeyboardButton(text="PyPi", url=info['PyPi']),
        InlineKeyboardButton(text="Home Page", url=info['HomePage'])
    ]
    return buttons


Bot.run()
