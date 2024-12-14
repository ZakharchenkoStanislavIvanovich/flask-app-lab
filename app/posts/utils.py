import json

POSTS_FILE = 'posts.json'

def load_posts():
    """Завантаження постів із JSON-файлу"""
    try:
        with open(POSTS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_posts(posts):
    """Збереження постів у JSON-файл"""
    with open(POSTS_FILE, 'w') as file:
        json.dump(posts, file, indent=4)
