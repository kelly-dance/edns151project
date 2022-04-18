from typing import Dict, List, TypedDict
from datetime import datetime
import json
import os.path

# Type Defs
class Item(TypedDict):
    last_update: int
    expire_time: int
    name: str
    id: int

class DB(TypedDict):
    items: Dict[int, Item]

# db setup stuff
DB_PATH = 'db.json'

_db: DB = { 'items': {} }

if os.path.exists(DB_PATH):
    print('before')
    with open(DB_PATH, 'r') as f:
        _db = json.loads(f.read())
    print('after')
    print(len(_db['items']))

def _save_db():
    with open(DB_PATH, 'w') as f:
        f.write(json.dumps(_db))

# Exported functions for interacting with database

def add_item(expiration: int, name: str, save=True) -> int:
    """
    expiration is a posix timestamp

    id is created by hashing the expiration and name so
    so duplicates with same name / expiration date cannot be added
    (This simplifies qr reading, but may be a limitation)

    Don't touch save, it was just there for testing
    """
    id = hash((expiration, name))
    _db['items'][id] = {
        'id': id,
        'expire_time': expiration,
        'last_update': int(datetime.now().timestamp()),
        'name': name,
    }
    if save: _save_db()
    return id

def delete_item(id: int) -> bool:
    """
    id to delete an item should be found on the object
    returned by fetch_display_items
    """
    present = id in _db['items']
    if present:
        del _db['items'][id]
        _save_db()
    return present


def fetch_display_items() -> List[Item]:
    """
    returns up to 20 items which are going to 
    expire the soonest
    should come sorted correctly
    """
    items = list(_db['items'].values())
    items.sort(key=lambda item: item['expire_time'])
    return items[0:20]

