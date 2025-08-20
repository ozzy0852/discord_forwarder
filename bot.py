import discord
from discord.ext import commands
import os

# Получаем значения из переменных окружения
TOKEN = os.getenv("TOKEN")
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))
THREAD_ID = int(os.getenv("THREAD_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Бот {bot.user} успешно запущен!")

@bot.event
async def on_message(message: discord.Message):
    # Игнорируем сообщения самого бота
    if message.author == bot.user:
        return

    # Проверяем, что сообщение пришло из исходного канала
    if message.channel.id == SOURCE_CHANNEL_ID:
        # Находим тред
        thread = message.guild.get_thread(THREAD_ID)
        if thread:
            # Формируем текст
            content = f"**{message.author.display_name}:** {message.content}" if message.content else None
            # Если есть файлы → прикрепляем
            files = [await attachment.to_file() for attachment in message.attachments] if message.attachments else None

            try:
                if content or files:
                    await thread.send(content=content, files=files)
                    print(f"➡ Сообщение от {message.author.display_name} переслано.")
                else:
                    print(f"⚠ Сообщение от {message.author.display_name} было пустым (ничего не переслано).")
            except Exception as e:
                print(f"❌ Ошибка при отправке сообщения: {e}")

    # Обрабатываем команды (!test и т.п.)
    await bot.process_commands(message)

bot.run(TOKEN)
