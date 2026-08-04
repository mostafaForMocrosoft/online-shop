from os import path

database_url = "sqlite:///database.sqlite3"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

SECRET_KEY = "ldklsakdl;kals;dklaskdlasdlkasl;dklasdl;kl;kasker239849824523%#$$#^#$&$$#!@#@%$^%%W#@$%^&*(^%$#$@!#@$%$$#@!".encode()

BASE_DIR = path.dirname(__file__)

UPLOAD_DIR = path.join(BASE_DIR, "static", "uploads")
