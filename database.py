# Модуль содержит функции по работе с базой данных
import pprint

import motor.motor_asyncio
from bson.objectid import ObjectId
from os import getenv
import asyncio

DB_LOGIN = getenv('DB_LOGIN')
DB_PASSWORD = getenv('DB_PASSWORD')
MONGO_DB = f'mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@itcube.jgcp4.mongodb.net/ITCube?retryWrites=true&w=majority'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB)
client.get_io_loop = asyncio.get_running_loop
database = client.itcube
users = database['users']


def user_helper(user) -> dict:
    # Метод являет собой модель записи пользователя в базе данных
    return {
        'id': str(user['_id']),
        'public_id': user['public_id'],
        'name': user['name'],
        'surname': user['surname'],
        'email': user['email'],
        'password': user['password'],
        'role': user['role'],
        'courses': user['courses'],
        'validated': user['validated'],
        'birthday': user['birthday'],
        'registration_date': user['registration_date']
    }


async def find_users() -> list:
    # Метод возвращает список пользователей, найденных по запросу
    cursor = await users.find()
    if cursor:
        founded = list([user_helper(user) for user in cursor])
        return founded


async def add_user(user_data: dict) -> dict:
    # метод добавляет пользователя в базу данных и возвращает его данные если добавление прошло удачно
    user = await users.insert_one(user_data)
    new_user = await users.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def find_user(params: dict) -> dict:
    # метод ищет пользователя по запросу параметров
    user = await users.find_one(params)
    if user:
        return user_helper(user)


async def update_user(email: str, data: dict) -> bool:
    # метод изменяет данные пользователя в базе данных
    if len(data) < 1:
        return False
    user = await users.find_one({"email": email})
    if user:
        updated_user = await users.update_one(
            {"email": email}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def delete_user(email: str):
    # метод удаляет пользователя из базы данных
    user = await users.find_one({"email": email})
    if user:
        await users.delete_one({"email": email})
        return True