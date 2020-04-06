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

import requests

import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token=TELEGRAM_TOKEN)
server = Flask(__name__)

BEST_TOKEN = os.environ['BEST_TOKEN']

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
def handle_start(message):
    bot.send_message(message.chat.id, '👋🏻')

@bot.message_handler(commands=['help']) # help message handler
def handle_help(message):
    bot.reply_to(message, 'We are still developing this bot 😉')

@bot.message_handler(commands=['connect']) # connect message handler
def handle_connect(message):
    bot.send_message(message.chat.id, 'Follow this link: https://pa.best.eu.org/webhook/telegram.jsp?user='+str(message['from']['id']))

@bot.message_handler(commands=['whois']) # whois message handler
def handle_whois(message):
    user_id = message.text[6:].strip()
    result = requests.get('https://www.best.eu.org/webhook/whois.jsp?token='+BEST_TOKEN+'&person='+user_id)
    if result.status_code != 200:
        bot.reply_to(message, 'Please send me a user id')
        return result.status_code
    if result.text.strip() == '':
        bot.reply_to(message, 'I couldn\'t find the person you are looking for')
        return 404
    user = result.json()
    reply = user['firstname'] + ' ' + user['lastname']
    bot.reply_to(message, reply)

################################################################

@server.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://technockickenbot.herokuapp.com/' + TELEGRAM_TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))