import telebot
from moviepy.editor import *
from pytube import YouTube
from telebot.types import *
import requests

TOKEN = 'Your token'


def download_video(message: Message):
    try:
        url = message.text.strip()
        yt = YouTube(url)
        video = yt.streams.get_lowest_resolution()
        bot.reply_to(message, "Скачиваю...")
        video.download(filename="video.mp4")
        bot.reply_to(message, "Done")
        bot.send_message(message.chat.id, "Что дальше? В конце обязательно выйди!", reply_markup=buttons)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Что-то не так. Проверь свой url")


bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Дай кота'))
keyboard.add(KeyboardButton('Конвертировать видео'))
buttons = InlineKeyboardMarkup()
buttons.add(InlineKeyboardButton('Получить видео🎥', callback_data='get_video'))
buttons.add(InlineKeyboardButton('Получить аудио🎶', callback_data='get_audio'))
buttons.add(InlineKeyboardButton('Выйти', callback_data='exit'))


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет. Чтобы конвертировать видео из Youtube в аудио, нажми соотвествующую кнопку', reply_markup=keyboard)


@bot.message_handler(regexp=r'Конвертировать видео.*')
def converter(message):
    bot.send_message(message.chat.id, "Скопируй url видео:")
    bot.register_next_step_handler(message, download_video)


@bot.callback_query_handler(func=lambda callback: True)
def callback_sender(callback):
    if callback.data == 'get_video':
        try:
            file = open('video.mp4', 'rb')
            bot.send_message(callback.message.chat.id, "Посылаю видео")
            bot.send_video(callback.message.chat.id, video=file, timeout=10000)
            bot.send_message(callback.message.chat.id, "Готово")
            file.close()
        except Exception as e:
            print(e)
            bot.send_message(callback.message.chat.id, "Что-то не так")

    if callback.data == 'get_audio':
        try:
            audio = AudioFileClip("video.mp4")
            audio.write_audiofile("sound.mp3")
            file = open('sound.mp3', 'rb')
            bot.send_message(callback.message.chat.id, "Посылаю аудио")
            bot.send_audio(callback.message.chat.id, audio=file, timeout=10000)
            bot.send_message(callback.message.chat.id, "Готово")
            file.close()
        except Exception as e:
            print(e)
            bot.send_message(callback.message.chat.id, "Что-то не так")
    if callback.data == 'exit':
        try:
            bot.send_message(callback.message.chat.id, "Пока. Твои файлы удалены с сервера")
            os.remove("video.mp4")
            os.remove("sound.mp3")
        except Exception as e:
            pass


@bot.message_handler(func=lambda s: 'Дай кота' in s.text)
def send_cat(message):
    response = requests.get('https://cataas.com/cat')
    bot.send_photo(message.chat.id, response.content)


bot.infinity_polling()
