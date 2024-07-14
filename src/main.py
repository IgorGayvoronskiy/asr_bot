import io
import telebot
import functions
from telebot import types

api_token = '7488623562:AAGovSXy0qt1PUzFYWOAkbFMzGB30Qk9V4c'
bot = telebot.TeleBot(api_token)

pipe_s, pipe_q = functions.setup_model()
mode = True
model_mode = 's'


@bot.message_handler(commands=['work'])
def working_message(message):
    bot.send_message(message.chat.id, text=f'Опять работать...⁽⁽(੭ꐦ •̀Д•́ )੭*⁾⁾')
    global mode
    mode = True


@bot.message_handler(commands=['break'])
def break_message(message):
    bot.send_message(message.chat.id, text=f'Наконец-то отдых!🖐😉🤝🍻')
    global mode
    mode = False


@bot.message_handler(commands=['status'])
def break_message(message):
    if mode:
        bot.send_message(message.chat.id, text='Работа кипит!🎧✍🏭')
    else:
        bot.send_message(message.chat.id, text='Я сплю...💤🥱')


@bot.message_handler(commands=['keyboard'])
def keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("⚡Скорость")
    btn2 = types.KeyboardButton("💯Качество")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="{0.first_name},выбери режим работы:".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    global model_mode
    if message.text == "⚡Скорость":
        model_mode = 's'
    elif message.text == "💯Качество":
        model_mode = 'q'
    print(model_mode)


@bot.message_handler(content_types=['voice'])
def speech_recognition(message):
    if mode:
        voice_file = bot.get_file(message.voice.file_id)
        buf = io.BytesIO(bot.download_file(voice_file.file_path))
        buf.name = f"{message.from_user.id}.ogg"
        buf.seek(0)
        if model_mode == 's':
            prompt = functions.transcribe_audio(buf, pipe_s)
        else:
            prompt = functions.transcribe_audio(buf, pipe_q)
        bot.reply_to(message, text=prompt)


bot.polling(none_stop=True)
