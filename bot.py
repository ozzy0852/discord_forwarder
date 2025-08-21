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
        thread = message.guild.get_thread(THREAD_ID)
        if thread:
            try:
                # Текст
                content = message.content if message.content else None

                # Вложения
                files = [await a.to_file() for a in message.attachments] if message.attachments else None

                # Embeds (копируем их как есть)
                embeds = message.embeds if message.embeds else None

                if content or files or embeds:
                    await thread.send(content=content, files=files, embeds=embeds)
                    print(f"➡ Переслано сообщение из {message.channel.name}")
                else:
                    print(f"⚠ Пустое сообщение (ничего не переслано).")
            except Exception as e:
                print(f"❌ Ошибка при пересылке: {e}")

    await bot.process_commands(message)

bot.run(TOKEN)
