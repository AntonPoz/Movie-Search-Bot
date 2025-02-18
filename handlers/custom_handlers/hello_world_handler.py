from loader import bot
from telebot.types import Message


@bot.message_handler(commands=["hello-world"])
@bot.message_handler(func=lambda message: message.text.lower() == "привет")
async def handle_hello_world(message: Message):
    await bot.reply_to(
        message, f"Добро пожаловать в КиноБота! \n"
                 f"Чтобы начать работать со мной, "
                 f"необходимо выполнить следующую команду: /start"
    )
