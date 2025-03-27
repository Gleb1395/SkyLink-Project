import os

import django
import telebot
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from telebot import types

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


@bot.message_handler(commands=["start"])
def start_handler(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = types.KeyboardButton(text="Отправить контакт", request_contact=True)
    keyboard.add(button)
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для отправки билетов 🎫\nПоделись своим контактом, нажав кнопку ниже.",
        reply_markup=keyboard,
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    if message.contact:
        phone_number = message.contact.phone_number
        print(f"Получен телефон: {phone_number}")
        print(f"ID chat: {message.chat.id}")

        try:
            user = get_user_model().objects.get(phone=phone_number)
            bot.send_message(message.chat.id, f"Спасибо, {user.email}! Ваш контакт принят.")
            user.telegram_chat_id = message.chat.id
            user.save()
        except get_user_model().DoesNotExist:
            bot.send_message(message.chat.id, "Пользователь с таким номером не найден.")
    else:
        bot.send_message(message.chat.id, "Контакт не получен, попробуйте снова.")


if __name__ == "__main__":
    bot.polling(none_stop=False)
