from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import redis.asyncio as redis
import aiohttp
import asyncio

API_TOKEN = 'Твой BOT TOKEN'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация клиента Redis
redis_client = redis.from_url("redis://redis:6379")

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я ваш бот. Используйте команды /messages для получения сообщений и /add <сообщение> для добавления нового сообщения.")

@dp.message(Command('messages'))
async def messages_command(message: types.Message):
    cache_key = "messages_cache"
    messages = await redis_client.get(cache_key)

    if messages:
        messages = messages.decode('utf-8')
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://app:8000/api/v1/messages/") as response:
                data = await response.json()
                messages = "\n".join(f"Author: {msg['author']}, Content: {msg['content']}" for msg in data['messages'])
                await redis_client.set(cache_key, messages)

    await message.answer(f"Список сообщений:\n{messages}")

@dp.message(Command('add'))
async def add_command(message: types.Message):
    _, *msg_content = message.text.split()
    msg_content = " ".join(msg_content)
    if not msg_content:
        await message.answer("Пожалуйста, введите сообщение после команды /add.")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post("http://app:8000/api/v1/message/",
                                json={"content": msg_content, "author": message.from_user.username}) as response:
            result = await response.json()
            await message.answer(f"Сообщение добавлено: {msg_content}")

# Запуск бота
async def main():
    # Запуск диспетчера
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    # Запуск основного асинхронного процесса
    asyncio.run(main())
