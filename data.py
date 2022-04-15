from typing import Dict, List, TypedDict
from datetime import datetime
import json
import os.path
import math
import uuid

# Part 1
class Item(TypedDict):
    last_update: int
    expire_time: int
    name: str
    id: str

class DB(TypedDict):
    items: Dict[str, Item]

# Part 2
DB_PATH = 'db.json'

db: DB = { 'items': {} }


if os.path.exists(DB_PATH):
    print('before')
    with open(DB_PATH, 'r') as f:
        db = json.loads(f.read())
    print('after')
    print(len(db['items']))

def save_db():
    with open(DB_PATH, 'w') as f:
        f.write(json.dumps(db))

# Part 3
def add_item(expiration: int, name: str, save=True) -> str:
    id = str(uuid.uuid1())
    db['items'][id] = {
        'id': id,
        'expire_time': expiration,
        'last_update': math.floor(datetime.now().timestamp()),
        'name': name,
    }
    if save: save_db()
    return id

def delete_item(id: str) -> bool:
    present = id in db['items']
    if present:
        del db['items'][id]
        save_db()
    return present


def fetch_display_items() -> List[Item]:
    items = list(db['items'].values())
    items.sort(key=lambda item: item['expire_time'])
    return items[0:20]

