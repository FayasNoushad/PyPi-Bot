# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from pyrogram import Client


API = "https://api.abirhasan.wtf/pypi?query="


Bot = Client(
    "PyPi-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
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


Bot.run()
