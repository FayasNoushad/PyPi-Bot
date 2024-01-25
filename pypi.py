import requests
from requests.utils import requote_uri
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def details(query):
    try:
        # request to get json data
        r = requests.get(f"https://pypi.org/pypi/{requote_uri(query)}/json")
        r.raise_for_status()
        info = r.json()['info']
        # error=False, because no error here
        info['error'] = False
        return info

    except requests.exceptions.RequestException as e:
        # if any error found, returns error message as json data
        return {'error': f"Error fetching information for {query}: {e}"}


def pypi_text(query):
    
    info = details(query)
    
    if info['error']:
        return info.get['error']
    
    text = "--**Informations**--\n"
    
    text += f"\n**Package Name:** `{info['name']}`"
    text += f"\n**Author:** `{info['author']}`"
    
    if info['author_email']:
        text += f"\n**Author Email:** {info['author_email']}"
    
    text += f"\n**Summary:** `{info['summary']}`"
    text += f"\n**Required Python Version:** {info['requires_python']}"
    text += f"\n**Latest Version:** `{str(info['version'])}`"
    
    if info['license']:
        text += f"\n**License:** `{info['license']}`"
    
    return text


def pypi_buttons(query):
    
    info = details(query)
    feedback_button = [
        InlineKeyboardButton('⚙ Feedback ⚙', url='https://telegram.me/FayasNoushad')
    ]
    buttons = []
    
    # To checking error
    if info['error']:
        return InlineKeyboardMarkup([feedback_button])
    
    if info['home_page']:
        buttons.append(InlineKeyboardButton(text="Home Page", url=info['home_page']))
    
    if info['bugtrack_url']:
        buttons.append(InlineKeyboardButton(text="Bugtrack URL", url=info['bugtrack_url']))
    
    buttons.extend([
        InlineKeyboardButton(text="Package URL", url=info['package_url']),
        InlineKeyboardButton(text="Project URL", url=info['project_url'])
    ])
    
    project_urls = info['project_urls']
    
    # May be one or more project urls
    for i in project_urls:
        buttons.append(InlineKeyboardButton(text=i, url=project_urls[i]))
    
    # To arranging buttons
    arranged_buttons = []
    
    line = []
    for button in buttons:
        if len(line) < 2:
            line.append(button)
            # max no. of buttons in a line
            button_limit = 2
            if (len(line) == button_limit) or (button == buttons[-1]):
                arranged_buttons.append(line)
                line = []
        else:
            line = [button]
    
    # adding feedback button on last
    arranged_buttons.append(feedback_button)
    
    all_buttons = InlineKeyboardMarkup(arranged_buttons)
    
    # return all buttons
    return all_buttons
