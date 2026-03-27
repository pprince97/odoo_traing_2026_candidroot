import requests

BASE_URL = "http://localhost:8069/json/2"
API_KEY = 'ee918c000b8f4279c671920abef05d76c5532e4c'
headers = {
    "Authorization": f"bearer {API_KEY}",
    "X-Odoo-Database": "demo_library2",
    "User-Agent": "mysoftware " + requests.utils.default_user_agent(),
}
