from datetime import datetime
import os
from dotenv import load_dotenv

from db.config.config_db import session
from db.repositories.users_repository import UsersRepository
from db.repositories.groups_repository import GroupsRepository

load_dotenv()

# La lista de items sigue en texto por ahora
FILE_PATH = os.environ.get('FILE_PATH', 'archives/lists/list.txt')

def today() -> str:
    return datetime.now().date().strftime('%d-%m-%Y')

def items_format(items: str):
    items_list = items.split(',')
    return items_list

def read_items() -> list:
    items = []
    if not os.path.exists(FILE_PATH):
        return items

    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            items_content = items_format(line)
            items.append(
                {
                    'date': items_content[0],
                    'items': items_content[1:]
                }
            )
    return items

def message_format(message: str) -> str:
    date = today()
    items = message.replace("falta", "")
    return f'{date},{items}'

def add_items(message: str) -> None:
    # Ensure directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    items = message_format(message)
    with open(FILE_PATH, 'a', encoding='utf-8') as file:
        file.write(items)
        file.write('\n')

def delete_items() -> None:
    # Ensure directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, 'w', encoding='utf-8') as file:
        file.write('')

def add_chat_info(message, user):
    """
    Registra o actualiza al usuario y al grupo (si corresponde) en SQLite.
    Recibe los objetos Update.message y Update.message.from_user de python-telegram-bot.
    """
    chat_id = message.chat_id
    chat_type = message.chat.type

    # Register user
    users_repo = UsersRepository(session)
    users_repo.create_or_update_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        is_bot=user.is_bot
    )

    # Register group if it's a group
    if chat_type in ['group', 'supergroup']:
        chat_name = message.chat.title
        groups_repo = GroupsRepository(session)
        groups_repo.create_or_update_group(
            telegram_id=chat_id,
            title=chat_name,
            group_type=chat_type
        )
