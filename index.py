# bot = telebot.TeleBot("5418348343:AAHO52Ye58MMmxv8BG8TI0b8cjhjgSuCQSs")
# openai.api_key = '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'
# google_api_key = 'AIzaSyCLnjz9rxWVDTXYSG-vnTQzIB8-g2cGXD8'
# google_cse_id = '05692936d7f75485f'

import telebot
import wikipedia
import requests
import re
from googlesearch import search
from telebot import types

# Set up Wikipedia
wikipedia.set_lang("en")

# Set up Telegram Bot
API_TOKEN = '5418348343:AAHO52Ye58MMmxv8BG8TI0b8cjhjgSuCQSs'
bot = telebot.TeleBot(API_TOKEN)

# Set up Google Custom Search Engine (CSE) API
GOOGLE_API_KEY = 'AIzaSyCLnjz9rxWVDTXYSG-vnTQzIB8-g2cGXD8'
GOOGLE_CSE_ID = '05692936d7f75485f'

# Define command constants
START_COMMAND = '/start'
ASK_COMMAND = '/ask'
SEARCH_COMMAND = '/search'

# Define error messages
ERROR_MESSAGE = "Sorry, something went wrong. Please try again later."

# Define inline keyboard markup for menu
menu = types.InlineKeyboardMarkup()
menu.row(
    types.InlineKeyboardButton("Ask a question", callback_data='ask'),
    types.InlineKeyboardButton("Search Google", callback_data='search')
)

# Define handler for start command
@bot.message_handler(commands=[START_COMMAND])
def handle_start(message):
    # Send welcome message and menu
    bot.send_message(message.chat.id, "Hi! How can I help you today?", reply_markup=menu)

# Define handler for inline keyboard callback
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    # Define dictionary to map callback data to command
    command_map = {
        'ask': ASK_COMMAND,
        'search': SEARCH_COMMAND
    }
    # Check if callback data is valid
    if call.data in command_map:
        # Send command and placeholder
        command = command_map[call.data]
        bot.send_message(call.message.chat.id, f"Enter your {command[1:]} here:")
        bot.register_next_step_handler(call.message, eval(f"handle_{command[1:]}"))
    else:
        # Send error message
        bot.send_message(call.message.chat.id, ERROR_MESSAGE)

# Define handler for ask command
def handle_ask(message):
    # Try to get summary from Wikipedia
    try:
        page = wikipedia.page(message.text)
        summary = page.summary.split("\n")[0]  # Limit to first paragraph
        bot.send_message(message.chat.id, summary)
    except:
        # If summary not found, send error message
        bot.send_message(message.chat.id, ERROR_MESSAGE)

# Define handler for search command
def handle_search(message):
    # Try to search Google and send top 5 results
    try:
        query = message.text
        links = search(query, num_results=5)
        for link in links:
            bot.send_message(message.chat.id, link)
    except:
        # If search fails, send error message
        bot.send_message(message.chat.id, ERROR_MESSAGE)

# Start the bot
bot.polling()
