import telebot
from flask import Flask, request
import os
import urllib

import json
import codecs
import datetime
import os.path
import logging
import argparse


TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', None)
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
server = Flask(__name__)

################################################################

def findat(msg):
    # from a list of texts, it finds the one with the '@' sign
    for i in msg:
        if '@' in i:
            return i

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object

################################################################

@bot.message_handler(commands=['start']) # welcome message handler
def send_welcome(message):
    bot.send_message(message, '👋🏻')

@bot.message_handler(commands=['help']) # help message handler
def send_welcome(message):
    bot.reply_to(message, 'We are still developing this bot 😉')

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))