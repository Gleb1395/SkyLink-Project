import os

import django
import telebot
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from telebot import types

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from user.models import PendingTelegramTicket  # NOQA E402

token = os.getenv("TELEGRAM_TOKEN")
if token is None:
    token = "123456:dummy"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_handler(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_contact = types.KeyboardButton(text="Отправить контакт", request_contact=True)
    button_ticket = types.KeyboardButton(text="Получить билет")
    keyboard.add(button_contact, button_ticket)
    bot.send_message(
        message.chat.id,
        "Привет! Я бот для отправки билетов 🎫\n\n"
        "1️⃣ Нажми 'Отправить контакт', чтобы привязать свой аккаунт\n"
        "2️⃣ Или 'Получить билет', если ты уже отправлял контакт ранее",
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


@bot.message_handler(func=lambda message: message.text == "Получить билет")
def get_ticket_handler(message):
    try:
        user = get_user_model().objects.get(telegram_chat_id=message.chat.id)
    except get_user_model().DoesNotExist:
        bot.send_message(message.chat.id, "Пользователь не найден. Пожалуйста, сначала отправьте свой контакт.")
        return

    pending_tickets = PendingTelegramTicket.objects.filter(user=user, sent=False)

    if not pending_tickets.exists():
        bot.send_message(message.chat.id, "У вас нет доступных билетов.")
        return

    for ticket in pending_tickets:
        try:
            with open(ticket.pdf_path, "rb") as pdf_file:
                bot.send_document(message.chat.id, pdf_file, caption="Ваш билет 🎟️")
            ticket.sent = True
            ticket.save()
        except Exception as e:
            print("Ошибка отправки отложенного билета:", e)
            bot.send_message(message.chat.id, "Произошла ошибка при отправке билета. Попробуйте позже.")


if __name__ == "__main__":
    bot.polling(none_stop=False)
