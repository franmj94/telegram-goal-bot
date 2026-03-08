import os
import asyncio
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=TOKEN)

API_URL = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
API_KEY = os.getenv("API_KEY")

headers = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

async def check_matches():

    while True:

        try:

            response = requests.get(
                API_URL,
                headers=headers,
                params={"live": "all"}
            )

            data = response.json()

            for match in data["response"]:

                minute = match["fixture"]["status"]["elapsed"]

                if minute and 15 <= minute <= 40:

                    home = match["teams"]["home"]["name"]
                    away = match["teams"]["away"]["name"]

                    shots = match["statistics"][0]["statistics"][2]["value"]

                    if shots and shots >= 6:

                        message = f"""
⚽ POSIBLE GOL 1ª PARTE

{home} vs {away}

Minuto: {minute}

Tiros totales: {shots}

🔥 Alta presión ofensiva
"""

                        await bot.send_message(chat_id=CHAT_ID, text=message)

        except Exception as e:
            print(e)

        await asyncio.sleep(300)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot running')


def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), Handler)
    server.serve_forever()


threading.Thread(target=run_server).start()

asyncio.run(check_matches())
