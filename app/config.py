from os import path

BASE_DIR = path.abspath(path.dirname(path.dirname(__file__)))

database_url = f"sqlite:///{path.join(BASE_DIR, 'database.db3')}"