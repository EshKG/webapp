from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import redis.asyncio as redis
import asyncio

app = FastAPI()

# MongoDB и Redis настройки
mongo_client = MongoClient("mongodb://mongo:27017")
db = mongo_client.messages_db
collection = db.messages

redis_client = redis.from_url("redis://redis:6379")

class Message(BaseModel):
    content: str
    author: str

@app.get("/api/v1/messages/")
async def get_messages():
    messages = list(collection.find({}, {"_id": 0}))
    return {"messages": messages}

@app.post("/api/v1/message/")
async def post_message(message: Message):
    new_message = {
        "content": message.content,
        "author": message.author
    }
    collection.insert_one(new_message)
    # Очищаем кеш
    await redis_client.delete("messages_cache")
    return {"message": "Сообщение сохранено удачно!"}
